import os
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-db_old', help='api database in old kernel', required=True)
parser.add_argument('-db_new', help='api database in new kernel', required=True)
parser.add_argument('-db_obj', help='database of apis that need to be compared', required=False)
parser.add_argument('-output', help='database name of output', required=False)
args = parser.parse_args()

# check args
if not os.path.exists(args.db_old):
	print "[Error] database of elder kernel " + args.db_old + " isn't existed."
	quit()
else: 
	print "database of elder kernel is : " + args.db_old
if not os.path.exists(args.db_new):
	print "[Error] database of newer kernel " + args.db_new + " isn't existed."
	quit()
else: 
	print "database of newer kernel is : " + args.db_new
#if not os.path.exists(args.db_obj):
#	print "[Error] database of object " + args.db_obj + " isn't existed."
#	quit()
#else: 
#	print "database of object is : " + args.db_obj

# connect to database
conn_old = sqlite3.connect(args.db_old)
conn_new = sqlite3.connect(args.db_new)
if  args.db_obj:
	conn_obj = sqlite3.connect(args.db_obj)
cur_old = conn_old.cursor()
cur_new = conn_new.cursor()
if args.db_obj:
	cur_obj = conn_obj.cursor()

decls_obj = []
if args.db_obj:
	cur_obj.execute('select * from decls')
	decls_obj = cur_obj.fetchall()
	if len(decls_obj) == 0:
		print "[Error] read nothing from table decls of database " + args.db_obj
		quit()
else:
	cur_old.execute('select * from decls')
	decls_obj = cur_old.fetchall()

# create output database
OUTPUT_DB = ''
if args.output:
	OUTPUT_DB = args.output
else:
	OUTPUT_DB = 'output.db'
conn_out = sqlite3.connect(OUTPUT_DB)
cur_out = conn_out.cursor()
cur_out.execute('DROP TABLE IF EXISTS decls_chg')
cur_out.execute('CREATE TABLE IF NOT EXISTS decls_chg (name TEXT NOT NULL, file TEXT NOT NULL,\
 start_line INTEGER NOT NULL, kind INTEGER NOT NULL, old_decl TEXT NOT NULL,\
 old_file TEXT NOT NULL, new_decl TEXT NOT NULL, new_file TEXT NOT NULL,\
 type TEXT NOT NULL, PRIMARY KEY(name, file, start_line, kind, old_decl, new_decl, old_file, new_file))')
conn_out.commit()
print "output database is : " + OUTPUT_DB

# analyze the changes between elder kernel and newer kernel
print "Start analyzing..."

def table_insert(table_name, value_list):
#	print value_list
	if value_list[4].find("\'") >= 0:
		return True
		value_list[4] = value_list[4].replace("\'", "\\\'")
		print value_list
	if value_list[6].find("\'") >= 0:
		return True
		value_list[6] = value_list[6].replace("\'", "\\\'")
		print value_list
	if table_name == 'decls_chg':
		if len(value_list) != 9:
			print "[Error] value_list don't contain enough values to insert table decls_chg"
			return False
		if not cur_out.execute("INSERT INTO decls_chg VALUES('%s', '%s', %d, %d, '%s',\
 '%s', '%s', '%s', '%s')" % (value_list[0], value_list[1], value_list[2], value_list[3],\
 value_list[4], value_list[5], value_list[6], value_list[7], value_list[8])):
			print value_list
		return True

# filter reduplicated contents
def filter_decls(decls):
    if decls[0][0] == "task_struct":
       print decls[0][0]
    temp = decls[:]
    if decls[0][1] == 3:
        for d in decls:
            if (len(d[4]) - len(d[0])) <= 11:
                temp.remove(d)
    return temp

#def get_rel_path(abs_path):
#	if not abs_path.startswith('/'):
#		return abs_path
#	arch_pos = 0
#	include_pos = 0
#	kernel_pos = 0
#	if abs_path.find("")

NOT_FOUND = 'NOT FOUND'
decls_records = []
if args.db_obj:
	NAME = 1
	FILE = 0
	START_LINE = 2
	KIND = 6
else:
	NAME = 0
	FILE = 2
	START_LINE = 3
	KIND = 1
	
for d in decls_obj:
	if d[NAME] in decls_records:
		continue
	decls_records.append(d[NAME])
	sql_cmd = "select * from decls where name='%s' order by type" % d[NAME]
	value_list = []
	cur_old.execute(sql_cmd)
	cur_new.execute(sql_cmd)
	decls_old = cur_old.fetchall()
	decls_new = cur_new.fetchall()

        if d[NAME] == "task_struct":
            print d[NAME]
        if len(decls_old) > 1:
            decls_old = filter_decls(decls_old)[:]
        if len(decls_new) > 1:
            decls_new = filter_decls(decls_new)[:]
        if d[NAME] == "task_struct":
            print len(decls_old)
	if len(decls_old) == 0 and len(decls_new) == 0:
		print "[Warning] declaration \'" + d[NAME] + "\' isn't found in both old and new database."
		continue
	elif len(decls_old) == 0:
		value_list = [d[NAME], d[FILE], d[START_LINE], d[KIND], NOT_FOUND, NOT_FOUND, decls_new[0][4], decls_new[0][2], 'ADD']
		if not table_insert('decls_chg', value_list):
                        print "table_insert failed."
                        quit()
	elif len(decls_new) == 0:
		value_list = [d[NAME], d[FILE], d[START_LINE], d[KIND], decls_old[0][4], decls_old[0][2], NOT_FOUND, NOT_FOUND, 'DELETE']
		if not table_insert('decls_chg', value_list):
                        print "table_insert failed."
                        quit()
	elif len(decls_old) == len(decls_new):
                for i in range(len(decls_old)):
                        if os.path.basename(decls_old[i][2]) == os.path.basename(decls_new[i][2]) and decls_old[i][4] == decls_new[i][4]:
                                continue
                        else:
                                change_type = ''
                                if (not os.path.basename(decls_old[i][2]) == os.path.basename(decls_new[i][2])) and decls_old[i][4] == decls_new[i][4]:
                                        change_type = "FILE CHANGED"
                                elif os.path.basename(decls_old[i][2]) == os.path.basename(decls_new[i][2]) and (not decls_old[i][4] == decls_new[i][4]):
                                        change_type = "DECL CHANGED"
                                else:
                                        change_type = "ALL CHANGED"
				value_list = [d[NAME], d[FILE], d[START_LINE], d[KIND], decls_old[i][4], decls_old[i][2], decls_new[i][4], decls_new[i][2], change_type]
		                if not table_insert('decls_chg', value_list):
                                        print "table_insert failed."
                                        quit()

        else:
            if len(decls_old) > len(decls_new):
                less = decls_new
                more = decls_old
            else:
                less = decls_old
                more = decls_new
            for l in less:
                for m in more:
                    if l[1] == m[1] and os.path.basename(l[2]) == os.path.basename(m[2]):
                        if not l[4] == m[4]:
                            if len(decls_old) > len(decls_new):
                                value_list = [d[NAME], d[FILE], d[START_LINE], d[KIND], m[4], m[2], l[4], l[2], "DECL CHANGED"]
                            else:
                                value_list = [d[NAME], d[FILE], d[START_LINE], d[KIND], l[4], l[2], m[4], m[2], "DECL CHANGED"]
		            if not table_insert('decls_chg', value_list):
                                print "table_insert failed."
                                quit()
                        break

conn_out.commit()
print "Finished"

		




