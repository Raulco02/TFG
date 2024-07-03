import pytest
from flask import Flask, session
from http import HTTPStatus
from App.controllers.usuario_controller import usuario_blueprint
from App.services.usuario_service import usuarioService

# Crea una instancia de la aplicación Flask y registra el blueprint
app = Flask(__name__)
app.register_blueprint(usuario_blueprint, url_prefix='/usuario')
app.secret_key = 'test_secret_key'  # Necesario para usar sesiones

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

# def test_login_success(client):
#     response = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'password'})
#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {"message": "El usuario ha iniciado sesión correctamente"}

# def test_login_failure(client):
#     response = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'wrongpassword'})
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json == {'error': 'Usuario no encontrado'}

# def test_login_missing_data(client):
#     response = client.put('/usuario/login', json={'correo': 'test@user.com'})
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json == {'error': 'Faltan datos del usuario'}

# def test_obtener_perfil_success(client):
#     with client.session_transaction() as sess:
#         sess['register'] = True
#         sess['usuario_id'] = 1

#     response = client.get('/usuario/perfil')
#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {'id': 1, 'nombre': 'test', 'correo': 'test@user.com'}

def test_obtener_perfil_no_session(client):
    response = client.get('/usuario/perfil')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {'error': 'El usuario no tiene sesión o no está registrado'}

def test_obtener_perfil_not_found(client):
    with client.session_transaction() as sess:
        sess['register'] = True
        sess['usuario_id'] = 1

    response = client.get('/usuario/perfil')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'error': 'Usuario no encontrado'}

def test_registrar_success(client):
    ##registrar success
    response_success = client.post('/usuario/registrar', json={
        'nombre': 'test',
        'correo': 'test@user.com',
        'pwd1': 'password123',
        'pwd2': 'password123'
    })
    assert response_success.status_code == HTTPStatus.OK
    assert response_success.json == {"message": "Usuario registrado correctamente"}
    #registrar failure
    response_failure = client.post('/usuario/registrar', json={
        'nombre': 'test',
        'correo': 'test@user.com',
        'pwd1': 'password123',
        'pwd2': 'password123'
    })
    assert response_failure.status_code == HTTPStatus.BAD_REQUEST
    assert response_failure.json == {"error": "El correo ya está en uso"}
    #login__failure
    response_l_f = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'wrongpassword'})
    assert response_l_f.status_code == HTTPStatus.NOT_FOUND
    assert response_l_f.json == {'error': 'Usuario no encontrado'}
    #login_missing_data
    response_m_d = client.put('/usuario/login', json={'correo': 'test@user.com'})
    assert response_m_d.status_code == HTTPStatus.BAD_REQUEST
    assert response_m_d.json == {'error': 'Faltan datos del usuario'}
    #login_success
    response_l_s = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'password123'})
    assert response_l_s.status_code == HTTPStatus.OK
    assert response_l_s.json == {"message": "El usuario ha iniciado sesión correctamente"}
    #obtener_perfil_success
    # with client.session_transaction() as sess:
    #     sess['register'] = True
    #     sess['usuario_id'] = 1

    response_perfil = client.get('/usuario/perfil')
    assert response_perfil.status_code == HTTPStatus.OK
    #logout
    response_logout = client.post('/usuario/logout')
    assert response_logout.status_code == HTTPStatus.OK
    assert response_logout.json == {'message': 'Logout exitoso'}
    #login 2
    response_l_s = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'password123'})
    #borrar usuario
    response_delete = client.delete('/usuario/delete/'+response_perfil.json['id'])	
    assert response_delete.status_code == HTTPStatus.OK

# def test_registrar_existing_email(client):
#     response = client.post('/usuario/registrar', json={
#         'nombre': 'test',
#         'correo': 'test@user.com',
#         'pwd1': 'password123',
#         'pwd2': 'password123'
#     })
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json == {"error": "El correo ya está en uso"}

# def test_logout_success(client):
#     with client.session_transaction() as sess:
#         sess['register'] = True
#         sess['usuario_id'] = 1

#     response = client.post('/usuario/logout')
#     assert response.status_code == HTTPStatus.OK
#     assert response.json == {'message': 'Logout exitoso'}
