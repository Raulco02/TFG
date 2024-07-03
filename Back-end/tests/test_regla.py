# import json
# import pytest
# import secrets
# from http import HTTPStatus
# from flask import session
# from App import create_app
# from App.services.regla_service import reglaService
# from App.services.mysql_dispositivo_service import mysql_dispositivoService


# @pytest.fixture
# def app():
#     app = Flask(__name__)
#     app.secret_key = secrets.token_hex(32) 
#     app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
#     app.register_blueprint(usuario_blueprint, url_prefix='/usuario')
#     app.register_blueprint(seccion_blueprint, url_prefix='/seccion')
#     app.register_blueprint(tarjeta_blueprint, url_prefix='/tarjeta')
#     return app

# @pytest.fixture
# def client(app):
#     return app.test_client()

# # Función auxiliar para iniciar sesión de prueba
# def login_test_user(client):
#     response_success = client.post('/usuario/registrar', json={
#         'nombre': 'test',
#         'correo': 'test@user.com',
#         'pwd1': 'password123',
#         'pwd2': 'password123'
#     })
#     response_l_s = client.put('/usuario/login', json={'correo': 'test@user.com', 'password': 'password123'})
#     perfil = client.get('/usuario/datos')
#     return perfil.json

# def borrar_usuario(client, id):
#     response_delete = client.delete('/usuario/delete/'+id)	
#     assert response_delete.status_code == HTTPStatus.OK


# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     app.config['SECRET_KEY'] = 'test_secret_key'
#     with app.test_client() as client:
#         with app.app_context():
#             yield client

# @pytest.fixture
# def authenticated_client(client):
#     with client.session_transaction() as sess:
#         sess['register'] = True
#         sess['usuario_id'] = 1
#         sess['rol'] = 1  # Simulamos un usuario administrador
#     yield client

# def test_get_user_reglas(authenticated_client):
#     response = authenticated_client.get('/regla/getAll')
#     assert response.status_code == HTTPStatus.UNAUTHORIZED

# def test_create_user_regla(authenticated_client):
#     regla_data = {
#         "nombre": "Regla de prueba",
#         "criterios": [{"tipo": "d", "dispositivo_id": 1, "atributo_id": 1, "valor": 50, "comparador": ">"}],
#         "acciones": [{"atributo_id": 1, "dispositivo_id": 1, "accion_id": 1, "valor_accion": 25}]
#     }

#     response = authenticated_client.post('/regla/create', json=regla_data)
#     assert response.status_code == HTTPStatus.BAD_REQUEST

# def test_create_user_alerta(authenticated_client):
#     alerta_data = {
#         "nombre": "Alerta de prueba",
#         "criterios": [{"tipo": "d", "dispositivo_id": 1, "atributo_id": 1, "valor": 50, "comparador": ">"}],
#         "acciones": [{"atributo_id": 1, "dispositivo_id": 1, "accion_id": 2, "valor_accion": 25}]
#     }

#     response = authenticated_client.post('/regla/create_alerta', json=alerta_data)
#     assert response.status_code == HTTPStatus.BAD_REQUEST

# def test_delete_user_regla(authenticated_client):
#     response = authenticated_client.delete('/regla/delete/1')
#     assert response.status_code == HTTPStatus.UNAUTHORIZED

# # Añadir más pruebas según sea necesario para cubrir otros casos de uso y rutas

