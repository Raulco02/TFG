import pytest
import secrets
from http import HTTPStatus
from flask import Flask,session, url_for
from App.controllers.integracion_controller import integracion_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32) 
    app.register_blueprint(integracion_blueprint, url_prefix='/integracion')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Función auxiliar para iniciar sesión de prueba
def login_test_user(client, role=1, register=True):
    with client.session_transaction() as sess:
        sess['register'] = register
        sess['rol'] = role

def test_get_integraciones(client):
    login_test_user(client)
    response = client.get(url_for('integracion.get_integraciones'))
    assert response.status_code == HTTPStatus.OK

def test_get_integraciones_no_session(client):
    response = client.get(url_for('integracion.get_integraciones'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_integraciones_no_permission(client):
    login_test_user(client, role=2)
    response = client.get(url_for('integracion.get_integraciones'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_tipos(client):
    login_test_user(client)
    response = client.get(url_for('integracion.get_tipos'))
    assert response.status_code == HTTPStatus.OK

def test_get_tipos_no_session(client):
    response = client.get(url_for('integracion.get_tipos'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_get_tipos_no_permission(client):
    login_test_user(client, role=2)
    response = client.get(url_for('integracion.get_tipos'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_add_edit_delete_integracion(client):
    login_test_user(client)
    data = {
        "nombre": "Test Integracion",
        "nombre_script": "script_de_test.py",
        "script": "print('hello world')",
        "atributos": [
            {
                "nombre": "atributo1",
                "unidades": "units",
                "actuable": False,
                "tipo": "Sensor"
            }
        ]
    }
    response = client.post(url_for('integracion.add_integracion'), json=data)
    print(response.json['id'])
    assert response.status_code == HTTPStatus.OK
    # Editar integración
    edit_data = {
        "prev_nombre": "Test Integracion",
        "nombre": "Updated Integracion",
        "nombre_script": "updated_script.py",
        "script": "print('updated')",
        "atributos": [
            {
                "nombre": "atributo1",
                "unidades": "units",
                "actuable": False,
                "tipo": "Sensor"
            }
        ]
    }
    edit_response = client.put(url_for('integracion.edit_integracion'), json=edit_data)
    assert edit_response.status_code == HTTPStatus.OK

    delete_data = {"id": response.json['id']}
    response_delete = client.delete(url_for('integracion.delete_integracion'), json=delete_data)
    assert response_delete.status_code == HTTPStatus.OK

def test_add_integracion_invalid_data(client):
    login_test_user(client)
    data = {
        "nombre": "Test Integracion",
        "nombre_script": "script_de_test.py",
        "script": "print('hello world')",
        "atributos": "invalid"
    }
    response = client.post(url_for('integracion.add_integracion'), json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_delete_integracion_invalid_data(client):
    login_test_user(client)
    data = {}
    response = client.delete(url_for('integracion.delete_integracion'), json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
