# app/domain/services/user_service.py
import uuid

from app.domain.entities.userAccount import UserAccount
from app.domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, personal_id):
        return self.user_repository.get_user_by_id(personal_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, personal_id, institution_name,
                 identification_type_id, health_entity, interviewed_person, relationship,
                 interviewed_person_id, address, district_id, socioeconomic_status_id,
                 housing_type, referred_by, referral_address, referral_phones,
                 entity_organization, family_members, total_monthly_income,
                 referral_cause, support_request, observations):
        user_id = uuid.uuid4()

        new_user = UserAccount(
            user_id=user_id,
            personal_id=personal_id,
            institution_name=institution_name,
            identification_type_id=identification_type_id['identification_type_id'],
            health_entity=health_entity,
            interviewed_person=interviewed_person,
            relationship=relationship,
            interviewed_person_id=interviewed_person_id,
            address=address,
            district_id=district_id['district_id'],
            socioeconomic_status_id=socioeconomic_status_id['socioeconomic_status_id'],
            housing_type=housing_type,
            referred_by=referred_by,
            referral_address=referral_address,
            referral_phones=referral_phones,
            entity_organization=entity_organization,
            family_members=family_members,
            total_monthly_income=total_monthly_income,
            referral_cause=referral_cause,
            support_request=support_request,
            observations=observations,
        )
        self.user_repository.create_user(new_user)

        return new_user

    # Service to get referral cause, support requests and observations of a beneficiary by his id
    def get_additional_information_by_id(self, personal_id):
        return self.user_repository.get_additional_information_by_id(personal_id)

    # Service to update the information of a foundation worker by his id
    def update_foundation_worker_by_id(self, worker_id, data):
        return self.user_repository.update_foundation_worker_by_id(worker_id, data)

    # Service to get the clinical history of a user by their personal ID.
    #    personal_id (str): The personal ID of the user.
    def get_clinical_history_by_id(self, personal_id):
        return self.user_repository.get_clinical_history_by_id(personal_id)
    
    # Service to get all beneficiaries parcial information 
    def get_beneficiariesShortInfo(self):
        return self.user_repository.get_beneficiariesShortInfo()

    # Service to update the information of a beneficiary by his id
    def update_beneficiary_by_id(self, data):
        return self.user_repository.update_beneficiary_by_id(data)

    # Service to delete the additional information of a beneficiary by his id
    def delete_additional_information_by_id(self, personal_id):
        return self.user_repository.delete_additional_information_by_id(personal_id)
    
    # Service to add the addtional information of a beneficiary by his id
    def add_additional_information_by_id(self, data):
        return self.user_repository.add_additional_information_by_id(data)
    
    
    # Service to get the family member information by his unique id
    def get_family_member_user_by_unique_id(self, family_member_id):
        return self.user_repository.get_family_member_user_by_unique_id(family_member_id)

    # Service to get all family members of a user and the socioeconomic_status
    def get_family_group_user(self, personal_id):
        return self.user_repository.get_family_group_user(personal_id)

    # Service to create a family member for a user
    def create_family_member_user(self, family_member):
        return self.user_repository.create_family_member_user(family_member)

    # Service to update a family member of a user
    def update_family_member_user(self, family_member):
        return self.user_repository.update_family_member_user(family_member)

    # Service to delete the information of a family member
    def delete_family_member_user(self, family_member_id):
        return self.user_repository.delete_family_member_user(family_member_id)

    
    def upload_image_s3(self, personal_id, extension_file, file):
        return self.user_repository.upload_image_s3(personal_id, extension_file, file)

    def get_beneficiary_name_image(self, personal_id):
        return self.user_repository.get_beneficiary_name_image(personal_id)