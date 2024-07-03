import pytest
import secrets
from http import HTTPStatus
from flask import Flask, session, url_for
from App.controllers.dashboard_controller import dashboard_blueprint
from App.controllers.usuario_controller import usuario_blueprint
from App.controllers.seccion_controller import seccion_blueprint
from App.controllers.tarjeta_controller import tarjeta_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32) 
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(usuario_blueprint, url_prefix='/usuario')
    app.register_blueprint(seccion_blueprint, url_prefix='/seccion')
    app.register_blueprint(tarjeta_blueprint, url_prefix='/tarjeta')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Función auxiliar para iniciar sesión de prueba
def login_test_user(client):
    response_success = client.post('/usuario/registrar', json={
        'nombre': 'test',
        'correo': 'test@user.com',
        'pwd1': 'password123',
        'pwd2': 'password123'
    })
    response_l_s = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'password123'})
    perfil = client.get('/usuario/datos')
    return perfil.json

def borrar_usuario(client, id):
    response_delete = client.delete('/usuario/delete/'+id)	
    assert response_delete.status_code == HTTPStatus.OK

def test_create_texto(client):
    usuario = login_test_user(client)
    data = {
        "tipo": "Texto",
        "posicion": "1x1",
        "contenido": "Texto de prueba",
        "id_seccion": usuario['dashboards'][0]['secciones'][0]['id']
    }
    
    # Simular solicitud POST a la ruta /tarjeta/create_texto
    response = client.post('/tarjeta/create_texto', json=data)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert 'error' not in data
    borrar_usuario(client, usuario['usuario']['id'])

def test_get_tarjetas(client):
    usuario = login_test_user(client)
    data = {
        "tipo": "Texto",
        "posicion": "1x1",
        "contenido": "Texto de prueba",
        "id_seccion": usuario['dashboards'][0]['secciones'][0]['id']
    }
    response = client.post('/tarjeta/create_texto', json=data)
    # Simular solicitud POST a la ruta /tarjeta/create_texto
    response = client.get(f"/tarjeta/get/{usuario['dashboards'][0]['secciones'][0]['id']}")
    data = response.get_json()
    assert response.status_code == HTTPStatus.OK

    borrar_usuario(client, usuario['usuario']['id'])
