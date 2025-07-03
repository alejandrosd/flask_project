import requests
import os
import time

BACKEND_URL = 'http://localhost:3000/api/procesar_archivo'

def test_procesar_archivo_desde_fuera(tmp_path, monkeypatch):
    # 👉 Preparar contenido
    contenido = "línea uno\nlínea dos\nlínea tres"

    # 👉 Monkeypatch del OUTPUT_DIR si el repositorio lo permite (opcional)
    # Si no podés monkeypatchear, solo validás que devuelva éxito
    payload = {"contenido": contenido}

    # 👉 Hacer request real al endpoint
    response = requests.post(BACKEND_URL, json=payload)

    # 👉 Validar respuesta HTTP
    assert response.status_code == 200
    data = response.json()
    assert "Archivo procesado" in data["mensaje"]
    print("✔ El backend respondió correctamente:", data["mensaje"])

    # No podés validar el archivo si no controlás el OUTPUT_DIR
    # A menos que el endpoint devuelva el nombre del archivo o la ruta
