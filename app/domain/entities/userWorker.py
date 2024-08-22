from app.domain.entities.userLogin import UserLogin

class UserWorker(UserLogin):
    def __init__( self, worker_id, name, personal_id, phone, position, email, login_id, password, username ):
        UserLogin.__init__( self, login_id, personal_id, password, username )
        self.worker_id = worker_id
        self.name = name
        self.personal_id = personal_id
        self.phone = phone
        self.position = position
        self.email = email
    
    def to_dict(self):
        return {
            "worker_id" : self.worker_id,
            "name" : self.name,
            "personal_id" : self.personal_id,
            "phone" : self.phone,
            "position" : self.position,
            "email" : self.email
        }