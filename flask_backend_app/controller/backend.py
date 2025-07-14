from flask import Flask, request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from model.archive import Archive
from model.semantic_model import SemanticModel
import requests

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

@app.route('/api/procesar_archivo', methods=['POST'])
def procesar_archivo():
    data = request.get_json()
    contenido = data.get('contenido')
    parameters = data.get('parametros')
    net_config = data.get('red')
    print("CONTENIDO")
    print(contenido)

    print("PARAMETROS")
    print(parameters)

    print("red")
    print(net_config)
    #archive = Archive
    #archive.process_archive(contenido,parameters,net_config)
    semantic_model = SemanticModel
    model = semantic_model.construir_modelo_semantico(contenido,parameters,net_config)
    print("MODEL")
    print(model)

    semantic_model.generate_test_cases(model)
    test_file = "test_integration.py"
    resultado = semantic_model.ejecutar_tests(test_file)
    print("Contenido recibido en backend:", resultado["exit_code"])
    return jsonify({
        "Output": resultado["exit_code"]
    })

    # Procesar la cadena
    #print("Contenido recibido en backend:", contenido[:100])

    #return jsonify({'mensaje': 'Archivo procesado'})

@app.route('/backend_test_ms', methods=['POST'])
def backend_test_ms():
    URL = 'http://localhost:3000/other_test_ms'
    data = request.get_json()
    contenido = data.get('contenido')

    try:
        respuesta = requests.post(URL, json={'contenido': contenido,'prueba':"prueba"})
        return jsonify({'mensaje': 'procesado'})
    except Exception as e:
        return jsonify({'mensaje': 'Error al contactar el backend', 'error': str(e)}), 500



@app.route('/other_test_ms', methods=['POST'])
def other_test_ms():
    data = request.get_json()
    contenido = data.get('contenido')
    prueba = data.get('prueba')  # Nuevo parámetro

    # Procesar la cadena
    print("Contenido recibido en backend:", contenido)
    print("Prueba recibida en backend:", prueba)

    return jsonify({'mensaje': 'procesado'})

if __name__ == '__main__':
    app.run(port = 3000, debug = True,use_reloader=False)