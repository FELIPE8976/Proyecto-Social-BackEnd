import json

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS  # Importa CORS desde flask_cors


from app.common.auth import token_required
from app.common.config import Config
from app.domain.services.auth_service import AuthService
from app.infrastructure.database.sql_login_repository import SqlLoginRepository

app = Flask(__name__)
CORS(app)  # Aplica CORS a tu aplicación Flask


def login_api(data):
    with app.app_context():
        if not data or not data['personal_id'] or not data['password']:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        login_repository = SqlLoginRepository()
        auth_service = AuthService(login_repository, Config.SECRET_KEY)
        auth_result = auth_service.authenticate_user(data.get('personal_id'), data.get('password'))
        if 'token' in auth_result:
            return jsonify({'token': auth_result['token']})  # No decodificar el token

        return make_response(auth_result['error'], 401, {'WWW-Authenticate': 'Basic realm="Login required!"',
            "Access-Control-Allow-Origin": "*"})


@token_required
def create_login_user_api(event, context):
    with app.app_context():
        try:
            user_data = json.loads(event['body'])
            login_repository = SqlLoginRepository()
            login_service = AuthService(login_repository, Config.SECRET_KEY)
            login_user = login_service.create_user(user_data['name'], user_data['personal_id'], user_data['phone'], 
                    user_data['position'], user_data['email'], user_data['password'], user_data['username'],)

            return {
                "statusCode": 201,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": "Created"
            }
        except Exception as e:
            # Manejo de errores, como datos inválidos, conflictos, etc.
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": str(e)})
            }


def get_name_by_personal_id_api(event, context):
    with app.app_context():
        user_id = event['pathParameters']['id']
        login_repository = SqlLoginRepository()
        login_service = AuthService(login_repository, Config.SECRET_KEY)
        name = login_service.get_name_by_personal_id(user_id)
        name_dict = {'name': name}

        if name is None:
            return {
                "statusCode": 401,
                "body": json.dumps({'message': 'Name not found'}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        return {
            "statusCode": 200,
            "body": json.dumps(name_dict),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"

            }
        }

