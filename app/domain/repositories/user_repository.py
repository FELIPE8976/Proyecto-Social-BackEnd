# app/domain/repositories/user_repository.py

from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, personal_id):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def create_user(self, user_account):
        pass

    # Method to get referral cause, support requests and observations of a beneficiary by his id
    @abstractmethod
    def get_additional_information_by_id(self, personal_id):
        pass

    # Method to update the information of a foundation worker by his id
    @abstractmethod
    def update_foundation_worker_by_id(self, worker_id, data):
        pass

    # Method to get the clinical history of a user by their personal ID
    @abstractmethod
    def get_clinical_history_by_id(self, personal_id):
        pass

    # Method to get all beneficiaries parcial information 
    @abstractmethod
    def get_beneficiariesShortInfo(self):
        pass
    
    # Method to update the information of a beneficiary by his id
    @abstractmethod
    def update_beneficiary_by_id(self, data):
        pass

    # Method to delete the additional information of a beneficiary by his id
    @abstractmethod
    def delete_additional_information_by_id(self, personal_id):
        pass

    # Method to add the additional information of a beneficiary by his id
    @abstractmethod
    def add_additional_information_by_id(self, data):
        pass
    
    # Method to get the family member information by his unique id
    @abstractmethod
    def get_family_member_user_by_unique_id(self, family_member_id):
        pass    

    # Method to upload the image link by his id
    @abstractmethod
    def upload_image_s3(self, personal_id, extension_file, file):
        pass

    # Method to get all the family members of a user and their socioeconomic status
    @abstractmethod
    def get_family_group_user(self, personal_id):
        pass

    # Method that creates a family member
    @abstractmethod
    def create_family_member_user(self, family_member):
        pass

    # Method that updates the information of a family member
    @abstractmethod
    def update_family_member_user(self, family_member):
        pass

    # Method that deletes the information of a family member
    @abstractmethod
    def delete_family_member_user(self, family_member_id):
        pass

    @abstractmethod
    def get_beneficiary_name_image(self, personal_id):
        pass

    @abstractmethod
    def get_all_departments(self):
        pass
