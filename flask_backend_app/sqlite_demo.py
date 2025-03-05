import sqlite3

#conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('employee.db')

c = conn.cursor()

#c.execute("""CREATE TABLE client (
#         doc_num INTEGER,
#         first_name TEXT,
#         last_name TEXT,
#         email TEXT,
#         phone_num INTEGER
#         )""")
#
#c.execute("""CREATE TABLE shopping (
#         shopping_id INTEGER,
#         shopping_cost INTEGER,
#         client_doc_num INTEGER
#         )""")
#
#c.execute("""CREATE TABLE doc_type (
#         doc_type_id INTEGER,
#         doc_type_name TEXT
#         )""")
c.execute("INSERT INTO client VALUES (1006015783,'Luis','Ocampo','luis.oc@gmail.com', 3134807368)")
#c.execute("INSERT INTO shopping VALUES (1,10000,1234)")
c.execute("INSERT INTO shopping VALUES (5,50000001,1006015783)")
#
c.execute("""SELECT * FROM shopping S""")
print(c.fetchall())
c.execute("""SELECT * from client C""")
print(c.fetchall())
c.execute("""SELECT C.doc_num, sum(S.shopping_cost) 
          FROM shopping S, client C
          WHERE S.client_doc_num = C.doc_num 
          GROUP BY C.doc_num
          HAVING sum(S.shopping_cost) > 5000000""")
print(c.fetchall())
conn.commit()
conn.close()