#!/usr/bin/python

import os
import sqlite3
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-db1', help='first database', required=True)
parser.add_argument('-db2', help='second database', required=True)
parser.add_argument('-source1', help='first driver source directory', required=True)
parser.add_argument('-source2', help='second driver source directory', required=True)
parser.add_argument('-driver', help='driver name', required=True)
args = parser.parse_args()

conn1 = sqlite3.connect(args.db1)
conn2 = sqlite3.connect(args.db2)
cur1 = conn1.cursor()
cur2 = conn2.cursor()

# sql search condition
#print "[Phase 1]looking for headers in deps which were included by driver sources..."
#cond = args.driver + "/%"
#cur1.execute('select * from deps where header like "%s"' % cond)
#deps1 = cur1.fetchall()
#cur2.execute('select * from deps where header like "%s"' % cond)
#deps2 = cur2.fetchall()
#print "[Result]deps1:", len(deps1), "deps2:", len(deps2)

print "[Phase 1]read decls and macros from database1 and database2"
decls1 = []
macros1 = []
#for d in deps1:
#    if d[1].find(args.driver) >= 0 :
#        continue
#    cond = "%" + d[1]
#    cur1.execute('select * from decls where header like "%s"' % cond)
#    tmp = cur1.fetchall()
#    if len(tmp) > 0:
#        decls1 += tmp
#    cur1.execute('select * from macros where header like "%s"' % cond)
#    tmp = cur1.fetchall()
#    if len(tmp) > 0:
#        macros1 += tmp

decls2 = []
macros2 = []
#for d in deps2:
#    if d[1].find(args.driver) >= 0 :
#        continue
#    cond = "%" + d[1]
#    cur2.execute('select * from decls where header like "%s"' % cond)
#    tmp = cur2.fetchall()
#    if len(tmp) > 0:
#        decls2 += tmp
#    cur2.execute('select * from macros where header like "%s"' % cond)
#    tmp = cur2.fetchall()
#    if len(tmp) > 0:
#        macros2 += tmp

# test
cur1.execute('select * from decls where header not like \"%' +  args.driver + '/%\"')
decls1 = cur1.fetchall()
cur1.execute('select * from macros where header not like \"%' +  args.driver + '/%\"')
macros1 = cur1.fetchall()
cur2.execute('select * from decls where header not like \"%' +  args.driver + '/%\"')
decls2 = cur2.fetchall()
cur2.execute('select * from macros where header not like \"%' +  args.driver + '/%\"')
macros2 = cur2.fetchall()

print "[Result]decls1:", len(decls1), "decls2:", len(decls2), "macros1:", len(macros1), "macros2:", len(macros2)

# delete declarations which were not called by driver code directly
print "[Phase 2]filter declarations and macros which were not called by driver directly"
cur_dir = os.getcwd()
if not os.path.isdir(os.path.abspath(args.source1)):
    print 'the first source argument is not a directory:', args.source1
    quit()
print "Now change to dir", args.source1
os.chdir(args.source1)
tmp = decls1[:]
for d in tmp:
#    print 'grep "%s" ./*' % d[1]
    if not os.system('grep "\W%s\W" ./* > /tmp/null' % d[1]) == 0:
#        print "####found and remove a indirect declaration:", d
        decls1.remove(d)
        continue
tmp = macros1[:]
for m in tmp:
#    print 'grep "%s" ./*' % m[1]
    if not os.system('grep "\W%s\W" ./* > /tmp/null' % m[1]) == 0:
#        print "####found and remove a indirect macro:", m
        macros1.remove(m)
        continue

os.chdir(cur_dir)
if not os.path.isdir(os.path.abspath(args.source2)):
    print 'the second source argument is not a directory:', args.source2
    quit()
os.chdir(args.source2)
print "Now change to dir", args.source2
tmp = decls2[:]
for d in tmp:
#    print 'grep "%s" ./*' % d[1]
    if not os.system('grep "\W%s\W" ./* > /tmp/null' % d[1]) == 0:
#        print "####found and remove a indirect declaration:", d
        decls2.remove(d)
        continue
tmp = macros2[:]
for m in tmp:
#    print 'grep "%s" ./*' % m[1]
    if not os.system('grep "\W%s\W" ./* > /tmp/null' % m[1]) == 0:
#        print "####found and remove a indirect macro:", m
        macros2.remove(m)
        continue
print "[Result]decls1:", len(decls1), "decls2:", len(decls2), "macros1:", len(macros1), "macros2:", len(macros2)

# look for declarations which is in decls2 but not in decls1
print "[Phase 3]looking for differences between old version driver and new version driver"
api_need_add = decls2[:]
api_need_change = []
for d2 in decls2:
    for d1 in decls1:
        if d1[1] == d2[1] and os.path.split(d1[0])[1] == os.path.split(d2[0])[1]:
            # check the prototypes
            cur1.execute('select * from prototypes where name = "%s"' % d1[1])
            cur2.execute('select * from prototypes where name = "%s"' % d2[1])
            proto1 = cur1.fetchall()
            proto2 = cur2.fetchall()
            if len(proto1) == 0 or len(proto2) ==0:
#                print "****found a declaration which is in both decls1 and decls2:"
#                print "\t", d1, "\n\t", d2
                api_need_add.remove(d2)
                break
            pcount = 0
            for p1 in proto1:
                for p2 in proto2:
                    if p1[1] == p2[1]:
                        pcount += 1
                        break
            if pcount == len(proto1):
                api_need_add.remove(d2)
                break
            # prototypes are different
            api_need_add.remove(d2)
            api_need_change.append(d2)
                        
# remove repeated elements
api_need_add = list(set(api_need_add))
print "[Result]api_need_add:", len(api_need_add)
api_need_change = list(set(api_need_change))
print "[Result]api_need_change:", len(api_need_change)

# look for macros which is different beween decls1 and decls2
macro_need_add = macros2[:]
macro_need_change = []
for m2 in macros2:
    for m1 in macros1:
        if m1[1] == m2[1] and os.path.split(m1[0])[1] == os.path.split(m2[0])[1]:
            # check the prototypes
            cur1.execute('select * from prototypes where name = "%s"' % m1[1])
            cur2.execute('select * from prototypes where name = "%s"' % m2[1])
            proto1 = cur1.fetchall()
            proto2 = cur2.fetchall()
            if len(proto1) == 0 or len(proto2) ==0:
#                print "****found a declaration which is in both decls1 and decls2:"
#                print "\t", m1, "\n\t", m2
                macro_need_add.remove(m2)
                break
            pcount = 0
            for p1 in proto1:
                for p2 in proto2:
                    if p1[1] == p2[1]:
                        pcount += 1
                        break
            if pcount == len(proto1):
                macro_need_add.remove(m2)
                break
            # prototypes are different
            macro_need_add.remove(m2)
            macro_need_change.append(m2)

            #print "****found a declaration which is in both macros1 and macros2:"
            #print "\t", m1, "\n\t", m2
            #macro_need_add.remove(m2)
            #break
# remove repeated elements
macro_need_add = list(set(macro_need_add))
print "[Result]macro_need_add:", len(macro_need_add)
macro_need_change = list(set(macro_need_change))
print "[Result]macro_need_change:", len(macro_need_change)

# store results into file
#print "[Phase 4]storing results into file direct_decls.txt"
#os.chdir(cur_dir)
#f = open('direct_decls.txt', 'w+')
#for d in api_need_add:
#    f.write(d.__str__() + '\n')
#f.close()
#f = open('direct_macros.txt', 'w+')
#for m in macro_need_add:
#    f.write(m.__str__() + '\n')
#f.close()

# store results into database
print "[Phase 4]storing results into database difference.sqlite"
os.chdir(cur_dir)
conn = sqlite3.connect("difference.sqlite")
cur = conn.cursor()
cur.execute('drop table if exists decls_diff')
cur.execute('drop table if exists macros_diff')
cur.execute('create table decls_diff (header TEXT NOT NULL, name TEXT NOT NULL, start_line INTEGER, start_column INTEGER, end_line INTEGER, end_column INTEGER, kind INTEGER, from_macro INTEGER, has_body INTEGER, change_type TEXT, PRIMARY KEY(header, name, start_line, kind))')
cur.execute('create table macros_diff (header TEXT NOT NULL, name TEXT NOT NULL, start_line INTEGER, start_column INTEGER, end_line INTEGER, end_column INTEGER, change_type TEXT, PRIMARY KEY(header, name, start_line))')

for d in api_need_add:
    cur.execute('insert into decls_diff values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], "ADD"))
for d in api_need_change:
    cur.execute('insert into decls_diff values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], "CHANGE"))
for d in macro_need_add:
    cur.execute('insert into macros_diff values (?, ?, ?, ?, ?, ?, ?)', (d[0], d[1], d[2], d[3], d[4], d[5], "ADD"))
for d in macro_need_change:
    cur.execute('insert into macros_diff values (?, ?, ?, ?, ?, ?, ?)', (d[0], d[1], d[2], d[3], d[4], d[5], "CHANGE"))

conn.commit()

print "finished"
