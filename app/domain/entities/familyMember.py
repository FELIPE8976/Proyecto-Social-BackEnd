
class FamilyMember:
    def __init__(self, family_member_id, user_id, full_name, age, relationship, education_level, occupation, monthly_income):
        self.family_member_id = family_member_id
        self.user_id = user_id
        self.full_name = full_name
        self.age = age
        self.relationship = relationship
        self.education_level = education_level
        self.occupation = occupation
        self.monthly_income = monthly_income

    def to_dict(self):
        return {
            'family_member_id': self.family_member_id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'relationship': self.relationship,
            'education_level': self.education_level,
            'occupation': self.occupation,
            'monthly_income': self.monthly_income
        }

