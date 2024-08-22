from abc import ABC, abstractmethod


class LoginRepository(ABC):
    @abstractmethod
    def find_by_personal_id(self, personal_id):
        pass

    @abstractmethod
    def create_user(self, user_login):
        pass

    @abstractmethod
    def get_name_by_personal_id(self, personal_id):
        pass