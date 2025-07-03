import requests


BACKEND_URL = 'http://localhost:3000/api/procesar_archivo'
FRONTEND_URL = 'http://localhost:3001/subir_archivo'
def test_procesar_archivo():
    # Preparar contenido
    contenido = "línea uno\nlínea dos\nlínea tres"

    # se crea payload con el contenido previamente definido
    payload = {"contenido": contenido}

    # Hacer request al endpoint
    response = requests.post(FRONTEND_URL, json=payload)

    # respuesta HTTP
    assert response.status_code == 200
    data = response.json()
    assert "Archivo procesado" in data["mensaje"]
    print("✔ El backend respondió correctamente:", data["mensaje"])

def test_flujo():
    contenido = "hola\nmundo"
    response = requests.post("http://localhost:3001/subir_archivo", json={"contenido": contenido})

    assert response.status_code == 200
    data = response.json()
    assert "Archivo procesado" in data["mensaje"]