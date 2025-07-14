import requests


def test_frontend_test_ms_to_backend_test_ms_integration():
    URL = "http://localhost:3001/frontend_test_ms"
    payload = {
        
        "contenido": "prueba1",
        
        "prueba": "prueba2"
        
    }

    response = requests.post(URL, json=payload)

    assert response.status_code == 200
    assert response.json()

def test_backend_test_ms_to_other_test_ms_integration():
    URL = "http://localhost:3000/backend_test_ms"
    payload = {
        
        "test": "prueba3",
        
        "paramet": "prueba4"
        
    }

    response = requests.post(URL, json=payload)

    assert response.status_code == 200
    assert response.json()
