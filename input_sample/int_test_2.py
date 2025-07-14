import requests


BACKEND_URL = 'http://localhost:3000/backend_test_ms'
FRONTEND_URL = 'http://localhost:3001/frontend_test_ms'
def test_procesar_archivo():
    # Preparar contenido
    contenido = "línea uno\nlínea dos\nlínea tres"

    # se crea payload con el contenido previamente definido
    payload = {

            "contenido": "prueba1",

            "prueba": "prueba2"

        }

    # Hacer request al endpoint
    response = requests.post(FRONTEND_URL, json=payload)
    # respuesta HTTP
    assert response.status_code == 200
    data = response.json()
    #assert "Archivo procesado" in data["mensaje"]
    print(data)
    assert data
    print("✔ El backend respondió correctamente:", data["mensaje"])

'''
def test_flujo():
    contenido = "hola\nmundo"
    response = requests.post("http://localhost:3001/subir_archivo", json={"contenido": contenido})

    assert response.status_code == 200
    data = response.json()
    assert "Archivo procesado" in data["mensaje"]
'''
FRONTEND_URL = 'http://localhost:3001/subir_archivo'


def test_course_ms_to_professor_ms_integration():
    payload = {

            "contenido": "Test University"

        }
    response = requests.post(
        FRONTEND_URL,
        #"http://professor_ms/api/professor_mss",
        json=payload
    )
    assert response.status_code == 200
    assert response.json()