# auth.py
from flask import Flask, request, jsonify
import json
import jwt
from functools import wraps
from app.common.config import Config

app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated(event, context, *args, **kwargs):
        token = None

        # Extraer el token de autorización del diccionario 'event'
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')

        if auth_header:
            parts = auth_header.split()
            if parts[0].lower() == 'bearer' and len(parts) == 2:
                token = parts[1]
            else:
                return {
                    "statusCode": 401,
                    "body": json.dumps({'message': 'Token is missing or invalid!'}),
                    "headers": {
                        "Content-Type": "application/json"
                    }
                }

        # Si no hay token, retornar error
        if not token:
            return {
                "statusCode": 401,
                "body": json.dumps({'message': 'Token is missing!'}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        try:
            # Intentar decodificar el token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except:
            return {
                "statusCode": 401,
                "body": json.dumps({'message': 'Token is invalid!'}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        # Agregar el usuario actual al diccionario 'event'
        event['current_user'] = current_user

        return f(event, context, *args, **kwargs)

    return decorated