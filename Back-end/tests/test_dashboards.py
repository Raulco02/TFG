import pytest
import secrets
from http import HTTPStatus
from flask import Flask, session, url_for
from App.controllers.dashboard_controller import dashboard_blueprint
from App.controllers.usuario_controller import usuario_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32) 
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(usuario_blueprint, url_prefix='/usuario')
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
    perfil = client.get('/usuario/perfil')
    return perfil.json

def borrar_usuario(client, id):
    response_delete = client.delete('/usuario/delete/'+id)	
    assert response_delete.status_code == HTTPStatus.OK

def test_get_user_dashboards(client):
    id_usuario = login_test_user(client)
    response = client.get(url_for('dashboard.get_user_dashboards'))
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert 'error' not in data
    borrar_usuario(client, id_usuario['id'])

def test_get_user_dashboards_no_session(client):
    response = client.get(url_for('dashboard.get_user_dashboards'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'

# def test_get_user_dashboard(client):
#     id_usuario = login_test_user(client)
#     response = client.get(url_for('dashboard.get_user_dashboard', id=1))
#     assert response.status_code == HTTPStatus.OK
#     data = response.get_json()
#     assert 'error' not in data
#     borrar_usuario(client, id_usuario['id'])

# def test_get_user_dashboard_no_session(client):
#     id_usuario = login_test_user(client)
#     response = client.get(url_for('dashboard.get_user_dashboard', id=1))
#     assert response.status_code == HTTPStatus.UNAUTHORIZED
#     data = response.get_json()
#     assert data['error'] == 'El usuario no tiene sesión o no está registrado'
#     borrar_usuario(client, id_usuario['id'])

def test_create_user_dashboard(client):
    id_usuario = login_test_user(client)
    response = client.post(url_for('dashboard.create_user_dashboard'), json={'nombre': 'New Dashboard', 'icono': 'icon.png'})
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['message'] == 'Dashboard creado correctamente'
    borrar_usuario(client, id_usuario['id'])

def test_create_user_dashboard_no_session(client):
    response = client.post(url_for('dashboard.create_user_dashboard'), json={'nombre': 'New Dashboard', 'icono': 'icon.png'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'

def test_create_user_dashboard_invalid_data(client):
    id_usuario = login_test_user(client)
    response = client.post(url_for('dashboard.create_user_dashboard'), json={'icono': 'icon.png'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert data['error'] == 'Se debe especificar un nombre para crear un dashboard'
    borrar_usuario(client, id_usuario['id'])

def test_edit_user_dashboard(client):
    id_usuario = login_test_user(client)
    response = client.post(url_for('dashboard.create_user_dashboard'), json={'nombre': 'New Dashboard', 'icono': 'icon.png'})
    data = response.get_json()
    id_dashboard = data["datos"]["id_dashboard"]
    response = client.put(url_for('dashboard.edit_user_dashboard'), json={'id': id_dashboard, 'nombre': 'Edited Dashboard', 'icono': 'new_icon.png'})
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['message'] == 'Dashboard editado correctamente'
    borrar_usuario(client, id_usuario['id'])

def test_edit_user_dashboard_no_session(client):
    response = client.put(url_for('dashboard.edit_user_dashboard'), json={'id': 1, 'nombre': 'Edited Dashboard', 'icono': 'new_icon.png'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'

def test_edit_user_dashboard_invalid_data(client):
    id_usuario = login_test_user(client)
    response = client.put(url_for('dashboard.edit_user_dashboard'), json={'id': 1, 'icono': 'new_icon.png'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert data['error'] == 'Se debe especificar un nombre para crear un dashboard'
    borrar_usuario(client, id_usuario['id'])

def test_delete_user_dashboard(client):
    id_usuario = login_test_user(client)
    response = client.post(url_for('dashboard.create_user_dashboard'), json={'nombre': 'New Dashboard', 'icono': 'icon.png'})
    data = response.get_json()
    id_dashboard = data["datos"]["id_dashboard"]
    response = client.delete(url_for('dashboard.delete_user_dashboard', id=id_dashboard))
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['message'] == 'Dashboard eliminado correctamente'
    borrar_usuario(client, id_usuario['id'])

def test_delete_user_dashboard_no_session(client):
    response = client.delete(url_for('dashboard.delete_user_dashboard', id=1))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'
