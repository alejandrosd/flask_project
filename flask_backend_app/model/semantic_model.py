from jinja2 import Environment, FileSystemLoader
import os, re, pytest, io, sys


class SemanticModel:
    def __init__(self):
        pass
    def construir_modelo_semantico(contenido_adl: str, parametros: dict, red: dict) -> dict:
        modelo = {
            "components": {},
            "relations": []
        }

        # Extraer componentes con parámetros
        matches = re.findall(r"component\s+(\w+)\(([^)]*)\)", contenido_adl)
        for nombre, params_str in matches:
            param_list = [p.strip() for p in params_str.split(',') if p.strip()]
            modelo["components"][nombre] = {
                "params": parametros.get(nombre, {}),
                "host": red.get(nombre, {}).get("host", "localhost"),
                "port": red.get(nombre, {}).get("port", 8000),
            }
            host = modelo["components"][nombre]["host"]
            port = modelo["components"][nombre]["port"]
            modelo["components"][nombre]["endpoint"] = f"http://{host}:{port}/{nombre}"

        # Extraer relaciones tipo: attachment (HTTP:frontend, backend)
        rel_matches = re.findall(r"attachment\s*\(([^:]+):([^,]+),\s*([^)]+)\)", contenido_adl)
        for connector, source, target in rel_matches:
            modelo["relations"].append({
                "connector": connector.strip(),
                "source": source.strip(),
                "target": target.strip()
            })

        return modelo
    def generate_test_cases(semantic_model):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("ms_to_ms_template.j2")

        output = template.render(
            components=semantic_model["components"],
            relations=semantic_model["relations"]
        )

        with open("test_integration.py", "w") as f:
            f.write(output)
    


    def ejecutar_tests(path_archivo):
        # Captura la salida
        stdout_original = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer

        # Ejecutar pytest como si fuera en consola
        try:
            result_code = pytest.main([path_archivo, "-q"])
        finally:
            sys.stdout = stdout_original

        salida = buffer.getvalue()
        buffer.close()
        print("SALIDA")
        print(salida)
        return {
            "exit_code": result_code,
            "output": salida
        }