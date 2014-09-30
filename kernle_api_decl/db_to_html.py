import sqlite3
import os

conn = sqlite3.connect('output.db')
cur = conn.cursor()
cur.execute('SELECT * FROM decls_chg')
results = cur.fetchall()

print "there are ", len(results), " results in database"

html = open("results.html", 'w')
html.write("""
<html>
<body>
     
<h1>The Results of Diff</h1>
        
<table border="1">
<tr>
  <th>name</th>
  <th>file</th>
  <th>start line</th>
  <th>kind</th>
  <th>old declaration</th>
  <th>old file</th>
  <th>new declaration</th>
  <th>new file</th>
  <th>change type</th>
</tr>
""")
       
for row in results:
    html.write("<tr>\n")
    for p in row:
        html.write("<td>%s</td>" % p)
    html.write("</tr>\n")

html.write("""
</table>
</body>
</html>
""")

os.system("google-chrome results.html")
