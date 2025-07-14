import requests

URL = 'http://localhost:3001/subir_archivo'


def test_course_ms_to_professor_ms_integration():
    payload = {
        
            "institution": ""
        
        }
    response = requests.post(
        URL,
        #"http://professor_ms/api/professor_mss",
        json=payload
    )
    assert response.status_code == 200
    assert response.json()

