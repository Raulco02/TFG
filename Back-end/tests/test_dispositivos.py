import pytest
import secrets
from http import HTTPStatus
from flask import Flask, session, url_for
from App.controllers.dispositivo_controller import dispositivo_blueprint
from App.controllers.integracion_controller import integracion_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32) 
    app.register_blueprint(dispositivo_blueprint, url_prefix='/dispositivo')
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

def test_get_dispositivos(client):
    response = client.get(url_for('dispositivo.get_dispositivos'))
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

def test_get_dispositivos_temperatura(client):
    response = client.get(url_for('dispositivo.get_dispositivos_temperatura'))
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

def test_get_dispositivos_por_atributo(client):
    response = client.get(url_for('dispositivo.get_dispositivos_por_atributo', id='some_id'))
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

def test_get_dispositivos_por_atributo_id_vacio(client):
    response = client.get(url_for('dispositivo.get_dispositivos_por_atributo', id=''))
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_get_dispositivo(client):
    response = client.get(url_for('dispositivo.get_dispositivo', id='some_id'))
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

def test_create_edit_delete_dispositivo(client):
    login_test_user(client)
    data_integracion = {
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
    response_integracion = client.post(url_for('integracion.add_integracion'), json=data_integracion)
    create_data = {
        "id": "test_id",
        "nombre": "Test Dispositivo",
        "topic": "test/topic",
        "nombre_integracion": "Test Integracion",
        "ubicacion": "test_location",
        "topics_actuacion": [],
        "plantillas_actuacion": []
    }
    response_create = client.post(url_for('dispositivo.create_dispositivo'), json=create_data)
    assert response_create.status_code == HTTPStatus.OK or response_create.status_code == HTTPStatus.BAD_REQUEST
    edit_data = {
        "prev_id": "test_id",
        "id": "new_test_id",
        "nombre": "Updated Dispositivo",
        "topic": "updated/topic",
        "nombre_integracion": "Test Integracion",
        "ubicacion": "updated_location",
        "topics_actuacion": [],
        "plantillas_actuacion": []
    }
    response_edit = client.put(url_for('dispositivo.edit_dispositivo'), json=edit_data)
    assert response_edit.status_code == HTTPStatus.OK or response_edit.status_code == HTTPStatus.BAD_REQUEST
    response_delete = client.delete(url_for('dispositivo.delete_dispositivo', id='new_test_id'))
    assert response_delete.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

    delete_integracion_data = {"id": response_integracion.json['id']}
    response_delete = client.delete(url_for('integracion.delete_integracion'), json=delete_integracion_data)

def test_create_dispositivo_no_session(client):
    data = {
        "id": "test_id",
        "nombre": "Test Dispositivo",
        "topic": "test/topic",
        "nombre_integracion": "test_integracion",
        "ubicacion": "test_location",
        "topics_actuacion": [],
        "plantillas_actuacion": []
    }
    response = client.post(url_for('dispositivo.create_dispositivo'), json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_create_dispositivo_no_permission(client):
    login_test_user(client, role=2)
    data = {
        "id": "test_id",
        "nombre": "Test Dispositivo",
        "topic": "test/topic",
        "nombre_integracion": "test_integracion",
        "ubicacion": "test_location",
        "topics_actuacion": [],
        "plantillas_actuacion": []
    }
    response = client.post(url_for('dispositivo.create_dispositivo'), json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_delete_dispositivo_no_id(client):
    login_test_user(client)
    response = client.delete(url_for('dispositivo.delete_dispositivo', id=''))
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_get_all_atributos(client):
    response = client.get(url_for('dispositivo.get_all_atributos'))
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

