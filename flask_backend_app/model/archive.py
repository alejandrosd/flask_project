from pyparsing import Word, ParseResults, alphanums, Suppress, Group, Optional, delimitedList, OneOrMore, Keyword, Literal, ParseException
import json
from jinja2 import Environment, FileSystemLoader

class Archive:
    def __init__(self):
        pass

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
    def process_archive(archive,parameters,net_config):
        #convertir el texto a diccionario

        #obtener las partes que se necesitan del diccionario

        #
        #id: TC101
        #group: Account
        #name: Login Valid Credentials Returns Token
        #endpoint: /api/accounts/tokens
        #method: POST
        #preconditions:
        #- "User with email 'valid@test.com' exists"
        #request_body:
        #   email: "valid@test.com"
        #   password: "Val1d!Pass"
        #expected_response:
        #   status_code: 200
        #   body:
        #       userId: is string not empty
        #       token: is string not empty
        #       refreshToken: is string not empty
        
        semantic_model = Archive.parse_architecture_dsl(archive)
        semantic_model = Archive.clean_semantic_model(semantic_model)
        
        print("SEMANTIC MODEL",semantic_model["components"]["course_ms"])

        # Valores extraídos posteriormente
        param_values = {
            "contenido": "Test Contenido"
        }

        semantic_model = Archive.add_parameters(semantic_model, param_values)

        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("ms_to_ms_template.j2")
        output = template.render(components=semantic_model["components"], connectors=semantic_model["connectors"])

        print("OUTPUT")
        print(output)
        file_name = "test_file.py"
        test_file = open(file_name, "w")
        test_file.write(output)
        test_file.close()

        import subprocess
        resultado = subprocess.run(['pytest', file_name], capture_output=True, text=True, check=True)
        print('Rsultado prueba: ')
        print(resultado.stdout)

        print('PRUEBA DE CLASE DE PYTHON',archive)

        #print(semantic_model)
        print('end')

    # Clean up the semantic model to convert ParseResults to plain lists
    
'''
# Run the parser on example input
dsl_text = """
architecture EvolvedArchitecture {
    component-and-connector-view::
        elements{
            component course_ms();
            component professor_ms(institution);
            connector http HTTP;
        }
        relations{
            attachment (HTTP:course_ms, professor_ms);
        }
}
semantic_model = parse_architecture_dsl(dsl_text)
semantic_model
'''