

class UserLogin:
    def __init__(self, login_id, personal_id, password, username):
        self.login_id = login_id
        self.personal_id = personal_id
        self.password = password
        self.username = username

    def to_dict(self):
        return {
            "login_id": self.login_id,
            "personal_id": self.personal_id,
            "password": self.password,
            "username": self.username
        }
