from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from aspose import pycore
from aspose.cells import Workbook, SaveFormat, FileFormatType

app = Flask(__name__)

app.secret_key = 'mysecretkey'
id_to_find = ''

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/seleccion', methods=['POST'])
def seleccion():
    protocolo = request.form.get('protocolo')
    metodo = request.form.get('metodo')

    # Lógica: si seleccionó POST, redirige al index
    if metodo == 'post':
        return redirect(url_for('subida'))
    else:
        return "<h3>Por ahora solo está implementado POST</h3>"

@app.route('/subida')
def subida():
    return render_template('index.html')

@app.route('/subir_archivo', methods=['POST'])
def enviar_al_backend():
    BACKEND_URL = 'http://localhost:3000/api/procesar_archivo'
    data = request.get_json()
    contenido = data.get('contenido')
    parametros = data.get('parametros')
    red = data.get('red')

    print("parametros")
    print(parametros)

    print("red")
    print(red)

    try:
        # Redirigir al backend real
        respuesta = requests.post(BACKEND_URL, json={'contenido': contenido, 'parametros':parametros, 'red':red})
        return jsonify(respuesta.json()), respuesta.status_code
    except Exception as e:
        return jsonify({'mensaje': 'Error al contactar el backend', 'error': str(e)}), 500



@app.route('/frontend_test_ms', methods=['POST'])
def frontend_test_ms():
    BACKEND_URL = 'http://localhost:3000/backend_test_ms'
    data = request.get_json()
    contenido = data.get('contenido')

    try:
        # Redirigir al backend real
        respuesta = requests.post(BACKEND_URL, json={'contenido': contenido})
        return jsonify(respuesta.json()), respuesta.status_code
    except Exception as e:
        return jsonify({'mensaje': 'Error al contactar el backend', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port = 3001, debug = True)