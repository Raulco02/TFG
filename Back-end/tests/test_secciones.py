import pytest
import secrets
from http import HTTPStatus
from flask import Flask, session, url_for
from App.controllers.dashboard_controller import dashboard_blueprint
from App.controllers.usuario_controller import usuario_blueprint
from App.controllers.seccion_controller import seccion_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32) 
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(usuario_blueprint, url_prefix='/usuario')
    app.register_blueprint(seccion_blueprint, url_prefix='/seccion')
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

def test_get_sections(client):
    usuario = login_test_user(client)
    response = client.get(url_for('seccion.get_seccions', id_dashboard=usuario['dashboards'][0]['id']))
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert 'error' not in data
    borrar_usuario(client, usuario['usuario']['id'])

def test_get_sections_no_session(client):
    response = client.get(url_for('seccion.get_seccions', id_dashboard='dashboard_id_here'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'

def test_get_section(client):
    usuario = login_test_user(client)
    response = client.get(url_for('seccion.get_seccion', id_seccion=usuario['dashboards'][0]['secciones'][0]['id']))
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert 'error' not in data
    borrar_usuario(client, usuario['usuario']['id'])

def test_get_section_not_found(client):
    id_usuario = login_test_user(client)
    response = client.get(url_for('seccion.get_seccion', id_seccion='invalid_id'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene permisos para acceder a esta seccion'
    borrar_usuario(client, id_usuario['usuario']['id'])

def test_create_section(client):
    usuario = login_test_user(client)
    response = client.post(url_for('seccion.create_seccion'), json={
        'dashboard_id': usuario['dashboards'][0]['id'],
        'nombre': 'New Section',
        'icono': 'icon.png',
        'layout': 'g'
    })
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['message'] == 'Seccion creada correctamente'
    borrar_usuario(client, usuario['usuario']['id'])

def test_create_section_no_session(client):
    response = client.post(url_for('seccion.create_seccion'), json={
        'dashboard_id': 'dashboard_id_here',
        'nombre': 'New Section',
        'icono': 'icon.png',
        'layout': 'g'
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'

def test_create_section_invalid_data(client):
    id_usuario = login_test_user(client)
    response = client.post(url_for('seccion.create_seccion'), json={
        'icono': 'icon.png',
        'layout': 'g'
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert data['error'] == 'Se debe especificar un nombre para crear un seccion'
    borrar_usuario(client, id_usuario['usuario']['id'])
    

def test_edit_section(client):
    usuario = login_test_user(client)
    response_edit = client.put(url_for('seccion.edit_seccion'), json={
        'id': usuario['dashboards'][0]['secciones'][0]['id'],
        'dashboard_id': usuario['dashboards'][0]['id'],
        'nombre': 'Edited Section',
        'icono': 'new_icon.png',
        'layout': 'g'
    })
    assert response_edit.status_code == HTTPStatus.OK
    data = response_edit.get_json()
    assert data['message'] == 'Seccion creada correctamente'
    borrar_usuario(client, usuario['usuario']['id'])

def test_edit_section_no_session(client):
    response = client.put(url_for('seccion.edit_seccion'), json={
        'id': 'section_id_here',
        'dashboard_id': 'new_dashboard_id',
        'nombre': 'Edited Section',
        'icono': 'new_icon.png',
        'layout': 'new_layout_data'
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.get_json()
    assert data['error'] == 'El usuario no tiene sesión o no está registrado'

def test_edit_section_invalid_data(client):
    id_usuario = login_test_user(client)
    response = client.put(url_for('seccion.edit_seccion'), json={
        'id':  id_usuario['dashboards'][0]['secciones'][0]['id'],
        'icono': 'new_icon.png',
        'layout': 'new_layout_data'
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert data['error'] == 'Se debe especificar un nombre para crear un seccion'
    borrar_usuario(client, id_usuario['usuario']['id'])

# def test_delete_section(client):
#     id_usuario = login_test_user(client)
#     response_delete = client.delete(url_for('seccion.delete_seccion', id=id_usuario['dashboards'][0]['secciones'][0]['id']))
#     assert response_delete.status_code == HTTPStatus.OK
#     data = response_delete.get_json()
#     assert data['message'] == 'Sección eliminada correctamente'
#     borrar_usuario(client, id_usuario['usuario']['id'])

# def test_delete_section_no_session(client):
#     response = client.delete(url_for('seccion.delete_seccion', id='section_id_here'))
#     assert response.status_code == HTTPStatus.UNAUTHORIZED
#     data = response.get_json()
#     assert data['error'] == 'El usuario no tiene sesión o no está registrado'
