from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine("sqlite:///employee.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Exporta todos los clientes con mas de COP 5.000.000 en compras
@app.route('/export_clients', methods = ['GET'])
def export_clients():
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    
    c.execute("""SELECT C.doc_num, C.first_name, C.last_name, C.email, sum(S.shopping_cost) 
          FROM shopping S, client C
          WHERE S.client_doc_num = C.doc_num 
          GROUP BY C.doc_num
          HAVING sum(S.shopping_cost) > 5000000""")
    result = c.fetchall()
    return result

# Busca todos los clientes de la aplicación
@app.route('/search_clients', methods = ['GET'])
def search_clients():
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM client")
    result = c.fetchall()
    return result

# Busca un cliente en especifico por ID
@app.route('/search_client/<id>')
def search_client(id):
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    print("as:",id,":ad")
    c.execute("SELECT * FROM client WHERE doc_num=?", (id,))
    result = c.fetchall()
    return result

if __name__ == '__main__':
    app.run(port = 3000, debug = True)