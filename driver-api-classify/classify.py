import sqlite3
import os
import argparse
import classes

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', help='database file', required=True)
args = parser.parse_args()

conn = sqlite3.connect(args.database)
cur = conn.cursor()

# get table decls
cur.execute('select * from decls')
decls = cur.fetchall()
#cur.execute('alter table decls add class text')

print "[Phase]Classifying now..."

# set class dictionary
class_dic = classes.class_dict
# set class
update_flag = False
exception_flag = False
for x in decls:
    update_flag = False
    # check class
    # first step: classify by path
    for c in classes.class_order:
        #print c
        if not class_dic[c]['path']:
            continue
        # handle exception key words
        if class_dic[c]['exc']:
            for e in class_dic[c]['exc']:
                if x[1].find(e) >= 0:
                    exception_flag = True
                    break;
        if exception_flag:
            exception_flag = False
            continue
        for p in class_dic[c]['path']:
            if x[0].find(p) >= 0:
                cur.execute('update decls set class = ? where header = ? and name = ? and start_line = ? and kind = ?', (c, x[0], x[1], x[2], x[6]))  
                update_flag = True
                break
            if update_flag:
                break
        if update_flag:
            break
    
    if update_flag:
        continue

    # second step: classify by file
    for c in classes.class_order:
        if not class_dic[c]['file']:
            continue
        # handle exception key words
        if class_dic[c]['exc']:
            for e in class_dic[c]['exc']:
                if x[1].find(e) >= 0:
                    exception_flag = True
                    break;
        if exception_flag:
            exception_flag = False
            continue
        for p in class_dic[c]['file']:
            if os.path.split(x[0])[1].find(p) >= 0:
                cur.execute('update decls set class = ? where header = ? and name = ? and start_line = ? and kind = ?', (c, x[0], x[1], x[2], x[6]))
                update_flag = True
                break
            if update_flag:
                break
        if update_flag:
            break
        
    if update_flag:
        continue

    # third step: classify by func
    for c in classes.class_order:
        if not class_dic[c]['func']:
            continue
        for p in class_dic[c]['func']:
            if x[1].find(p) >= 0:
                 cur.execute('update decls set class = ? where header = ? and name = ? and start_line = ? and kind = ?', (c, x[0], x[1], x[2], x[6]))
                 update_flag = True
                 break
            if update_flag:
                 break
        if update_flag:
            break

conn.commit()
print "[Phase]Classify finished."
