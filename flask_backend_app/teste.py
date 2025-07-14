import test_class

instancia = test_class
instancia.imprimir_prueba()


dds documents
detail design specification documents
COP firewall
resources on the conoco side


{'components': 
    {
        'frontend_test_ms': 
        {
            'params': {}, 
            'host': 'localhost', 
            'port': 8000, 
            'endpoint': 'http://localhost:8000/frontend_test_ms'
        }, 
        'backend_test_ms': 
        {
            'params': {'contenido': 'prueba1', 'prueba': 'prueba2'}, 
            'host': 'localhost', 
            'port': 8000, 
            'endpoint': 'http://localhost:8000/backend_test_ms'
        }, 
        'other_test_ms': 
        {
            'params': {'test': 'prueba3', 'paramet': 'prueba4'}, 
            'host': 'localhost', 
            'port': 8000, 
            'endpoint': 'http://localhost:8000/other_test_ms'
        }
    }, 
    'relations': 
    [
        {'connector': 'HTTP', 'source': 'frontend_test_ms', 'target': 'backend_test_ms'}, 
        {'connector': 'HTTP', 'source': 'backend_test_ms', 'target': 'other_test_ms'}
    ]







{'components': 
    {  'frontend_test_ms': 
        {   'params': {}, 
            'host': 'localhost', 
            'port': 8001, 
            'endpoint': 'http://localhost:8001/frontend_test_ms'
        }, 
        'backend_test_ms': 
        {   'params': {'contenido': 'prueba1', 'prueba': 'prueba2'}, 
            'host': 'localhost', 
            'port': 8002, 
            'endpoint': 'http://localhost:8002/backend_test_ms'
        }, 
        'other_test_ms': 
        {   'params': {'test': 'prueba3', 'paramet': 'prueba4'}, 
            'host': 'localhost', 
            'port': 8003, 
            'endpoint': 'http://localhost:8003/other_test_ms'
        }
    }, 
    'relations': 
    [   {'connector': 'HTTP', 'source': 'frontend_test_ms', 'target': 'backend_test_ms'}, 
        {'connector': 'HTTP', 'source': 'backend_test_ms', 'target': 'other_test_ms'}]
}