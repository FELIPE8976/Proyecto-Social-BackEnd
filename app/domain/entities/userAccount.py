# app/domain/entities/userAccount.py

import uuid

class UserAccount:
    def __init__(self, user_id, personal_id, institution_name,
                 identification_type_id, health_entity, interviewed_person, relationship,
                 interviewed_person_id, address, district_id, socioeconomic_status_id,
                 housing_type, referred_by, referral_address, referral_phones,
                 entity_organization, family_members, total_monthly_income,
                 referral_cause, support_request, observations):
        self.user_id = user_id
        self.personal_id = personal_id
        self.institution_name = institution_name
        self.identification_type_id = identification_type_id  # Instance of IdentificationType
        self.health_entity = health_entity
        self.interviewed_person = interviewed_person
        self.relationship = relationship
        self.interviewed_person_id = interviewed_person_id
        self.address = address
        self.district_id = district_id  # Instance of District
        self.socioeconomic_status_id = socioeconomic_status_id  # Instance of SocioeconomicStatus
        self.housing_type = housing_type  # Instance of HousingType
        self.referred_by = referred_by
        self.referral_address = referral_address
        self.referral_phones = referral_phones
        self.entity_organization = entity_organization
        self.family_members = family_members  # List of FamilyMember instances
        self.total_monthly_income = total_monthly_income
        self.referral_cause = referral_cause
        self.support_request = support_request
        self.observations = observations

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'personal_id': self.personal_id,
            'institution_name': self.institution_name,
            'identification_type_id': self.identification_type_id,
            'health_entity': self.health_entity,
            'interviewed_person': self.interviewed_person,
            'relationship': self.relationship,
            'interviewed_person_id': self.interviewed_person_id,
            'address': self.address,
            'district_id': self.district_id,
            'socioeconomic_status_id': self.socioeconomic_status_id,
            'housing_type': self.housing_type,
            'referred_by': self.referred_by,
            'referral_address': self.referral_address,
            'referral_phones': self.referral_phones,
            'entity_organization': self.entity_organization,
            'family_members': [member.to_dict() for member in self.family_members] if self.family_members else [],
            'total_monthly_income': self.total_monthly_income,
            'referral_cause': self.referral_cause,
            'support_request': self.support_request,
            'observations': self.observations
        }