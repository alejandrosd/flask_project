from pyparsing import Word, ParseResults, alphanums, Suppress, Group, Optional, delimitedList, OneOrMore, Keyword, Literal, ParseException
import json
from jinja2 import Environment, FileSystemLoader

def parse_architecture_dsl(dsl_text):
    # DSL parsing elements
    identifier = Word(alphanums + "_")
    component_kw = Keyword("component")
    connector_kw = Keyword("connector")
    attachment_kw = Keyword("attachment")
    elements_kw = Keyword("elements")
    relations_kw = Keyword("relations")

    # Grammar for components with optional input parameters
    component_decl = Group(
        component_kw + identifier("name") + 
        Optional(Suppress("(") + Optional(delimitedList(identifier))("inputs") + Suppress(")")) + 
        Suppress(";")
    )

    # Grammar for connectors
    connector_decl = Group(
        connector_kw + identifier("name") + identifier("type") + Suppress(";")
    )

    # Grammar for attachments (connector:from,to)
    attachment_decl = Group(
        attachment_kw + Suppress("(") + identifier("connector") + Suppress(":") + identifier("from") + Suppress(",") + identifier("to") + Suppress(")") + Suppress(";")
    )

    # Grammar for elements and relations blocks
    elements_block = elements_kw + Suppress("{") + Group(OneOrMore(component_decl | connector_decl))("elements") + Suppress("}")
    relations_block = relations_kw + Suppress("{") + Group(OneOrMore(attachment_decl))("relations") + Suppress("}")

    # Full architecture grammar
    architecture_parser = (
        Keyword("architecture") + identifier("architecture_name") +
        Suppress("{") +
        Keyword("component-and-connector-view::") +
        elements_block + 
        relations_block +
        Suppress("}")
    )

    # Parsing the DSL
    parsed = architecture_parser.parseString(dsl_text, parseAll=True)

    # Construct semantic model
    semantic_model = {
        "architecture": parsed["architecture_name"],
        "components": {},
        "connectors": {}
    }

    # Process elements
    connector_name_map = {}
    for elem in parsed["elements"]:
        if elem[0] == "component":
            semantic_model["components"][elem["name"]] = {
                "inputs": elem.get("inputs", [])
            }
        elif elem[0] == "connector":
            name = elem[1]  # Logical name
            semantic_model["connectors"][name] = {
                "type": elem[2],
                "attachments": []
            }
            connector_name_map[elem[2]] = name  # Map type to logical name

    # Process relations
    for rel in parsed["relations"]:
        connector_type = rel["connector"]
        connector_name = connector_name_map.get(connector_type, connector_type)
        from_comp = rel["from"]
        to_comp = rel["to"]
        if connector_name in semantic_model["connectors"]:
            semantic_model["connectors"][connector_name]["attachments"].append([from_comp, to_comp])
        else:
            semantic_model["connectors"][connector_name] = {
                "type": connector_type,
                "attachments": [[from_comp, to_comp]]
            }

    return semantic_model
    
def clean_semantic_model(model):
    for comp in model["components"].values():
        if isinstance(comp["inputs"], ParseResults):
            comp["inputs"] = list(comp["inputs"])
    return model

def add_parameters(model, values):
    for comp_name, comp in model["components"].items():
        enriched_inputs = []
        for param in comp["inputs"]:
            enriched_inputs.append({
                "name": param,
                "value": values.get(param, "")
            })
        comp["inputs"] = enriched_inputs
    return model
# Función para enriquecer con información de red
def add_network_info(model, host_map, port_map):
    for comp_name, comp in model["components"].items():
        print("comp")
        print(comp)
        print("comp_name")
        print(comp_name)
        hostname = host_map.get(comp_name, "localhost")
        port = port_map.get(comp_name, 8000)
        comp["host"] = hostname
        comp["port"] = port
        comp["endpoint"] = f"http://{hostname}:{port}/{comp_name}"
    return model

model = """
architecture EvolvedArchitecture {
    component-and-connector-view::
        elements{
            component frontend_test_ms();
            component backend_test_ms(contenido, prueba);
            connector http HTTP;
        }
        relations{
            attachment (HTTP:frontend_test_ms, backend_test_ms);
        }
}
"""

semantic_model = parse_architecture_dsl(model)
semantic_model = clean_semantic_model(semantic_model)
        
print("SEMANTIC MODEL",semantic_model["components"])
print(len(semantic_model["components"]))
print(semantic_model["components"])

claves = []
valores = ["prueba1", "prueba2"]

param={}

microservices = []
# Iterar sobre pares clave-valor
for clave, valor in semantic_model["components"].items():
    print(f"Clave: {clave}, Valor: {valor}")
    microservices.append(clave)
    for etiqueta, input in valor.items():
        print(f"input: {input}")
        for i in input:
            print(i)
            claves.append(i)
print("CLAVES: ")
print(claves)
print("SEMANTIC MODEL")

for i in range(len(claves)):
    param[claves[i]]= valores[i]

print(param)
# Valores extraídos posteriormente
param_values = param

print("SEMANTIC MODEL")
semantic_model = add_parameters(semantic_model, param_values)
print(semantic_model)

hosts = ["localhost","localhost"]
ports = [3001, 3000]

host_map = {}
port_map = {}
for i in range(len(microservices)):
    host_map[microservices[i]] = hosts[i]
    port_map[microservices[i]] = ports[i]

print("hosts: ")
print(host_map)
print("ports: ")
print(port_map)

semantic_model = add_network_info(semantic_model, host_map, port_map)

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("template.j2")
output = template.render(components=semantic_model["components"], connectors=semantic_model["connectors"])

print("OUTPUT")
print(output)

file_name = "test_file.py"
test_file = open(file_name, "w")
test_file.write(output)
test_file.close()

import os
print(file_name)
print("test os")
os.system('pytest '+file_name)

import subprocess
resultado = subprocess.run(['pytest', file_name], capture_output=True, text=True, check=True)
print(resultado.stdout)