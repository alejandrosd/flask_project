from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from aspose import pycore
from aspose.cells import Workbook, SaveFormat, FileFormatType

app = Flask(__name__)

app.secret_key = 'mysecretkey'
id_to_find = ''

# Raiz de la aplicación
@app.route('/')
def Index():   
    return render_template('index.html')

# Busqueda de cliente
@app.route('/client', methods = ['POST'])
def client():
    if request.method == 'POST':
        doc_type = request.form['doc_type']
        doc_num = request.form['doc_num']
        print(doc_type)
        print(doc_num)
        global id_to_find
        id_to_find = doc_num
        print("id to find",id_to_find)
        #flash('Cliente encontrado con exito')
        #flash('Cliente encontrado ')
    return redirect(url_for('search'))

# Exportar cliente por id
@app.route('/export/<id>')
def search_client(id):
    url = "http://127.0.0.1:3000/search_client/"+id
    req = requests.get(url)
    print("JSON",req.json()[0][0])
    workbook = Workbook()
    worksheet = workbook.worksheets[0]
    worksheet.cells.get("A1").put_value("Cedula")
    worksheet.cells.get("B1").put_value("Nombre")
    worksheet.cells.get("C1").put_value("Apellido")
    worksheet.cells.get("D1").put_value("Correo")
    worksheet.cells.get("E1").put_value("Telefono")
    worksheet.cells.get("A2").put_value(req.json()[0][0])
    worksheet.cells.get("B2").put_value(req.json()[0][1])
    worksheet.cells.get("C2").put_value(req.json()[0][2])
    worksheet.cells.get("D2").put_value(req.json()[0][3])
    worksheet.cells.get("E2").put_value(req.json()[0][4])
    #worksheet.cells.get("B2").put_value("ValueB")
    workbook.save("reporte_individual.xls")
    return redirect(url_for('search'))

# Busca cliente 
@app.route('/search')
def search():
    global id_to_find
    url = "http://127.0.0.1:3000/search_client/"+id_to_find
    print("url:",url)
    req = requests.get(url)
    if req.status_code != 200 or len(req.json()) < 1:
        id_to_find = ''
        flash('No existe el cliente')
        return render_template('index.html')
    print("YD",len(req.json()))
    print(req.status_code)
    flash('Cliente encontrado')
    data = req.json()
    
    return render_template('index.html', contacts = data)

# exporta todos los clientes para fidelización
@app.route('/export_all')
def export_all():
    url = "http://127.0.0.1:3000/export_clients"
    req = requests.get(url)
    print("JSON",req.json())
    workbook = Workbook()
    worksheet = workbook.worksheets[0]
    worksheet.cells.get("A1").put_value("Cedula")
    worksheet.cells.get("B1").put_value("Nombre")
    worksheet.cells.get("C1").put_value("Apellido")
    worksheet.cells.get("D1").put_value("Correo")
    worksheet.cells.get("E1").put_value("Gastos en compras")

    for i in range(0,len(req.json())):
        print(req.json()[i][0])
        number = i+2
        worksheet.cells.get("A"+str(number)).put_value(req.json()[i][0])
        worksheet.cells.get("B"+str(number)).put_value(req.json()[i][1])
        worksheet.cells.get("C"+str(number)).put_value(req.json()[i][2])
        worksheet.cells.get("D"+str(number)).put_value(req.json()[i][3])
        worksheet.cells.get("E"+str(number)).put_value(req.json()[i][4])
        
    #worksheet.cells.get("B2").put_value("ValueB")
    workbook.save("reporte_fidelizacion.xls")
    return redirect(url_for('search'))

if __name__ == '__main__':
    app.run(port = 3001, debug = True)