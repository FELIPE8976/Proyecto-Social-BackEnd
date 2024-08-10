import uuid

import bcrypt
import jwt
import datetime

from app.domain.entities.userWorker import UserWorker

def encrypt_password(password):
    # Genera un salt y encripta la contraseña
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


class AuthService:
    def __init__(self, login_repository, secret_key):
        self.login_repository = login_repository
        self.secret_key = secret_key

    def authenticate_user(self, personal_id, password):
        login_user = self.login_repository.find_by_personal_id(personal_id)
        if login_user and bcrypt.checkpw(password.encode('utf-8'), login_user.password.encode('utf-8')):
            token = jwt.encode({
                'user': login_user.personal_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, self.secret_key, algorithm="HS256")
            return {'token': token}
        return {'error': 'Invalid credentials'}

    def create_user(self, name, personal_id, phone, position, email, password, username):
        encrypted_password = encrypt_password(password)
        user_id = uuid.uuid4()
        worker_id = uuid.uuid4()
        new_user = UserWorker( worker_id=worker_id, name=name, personal_id=personal_id, 
                              phone=phone, position=position, email=email, login_id=user_id, password=encrypted_password, username=username)
        self.login_repository.create_user(new_user)
        return new_user

    def get_name_by_personal_id(self, personal_id):
        return self.login_repository.get_name_by_personal_id(personal_id)




