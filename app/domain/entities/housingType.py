
class HousingType:
    def __init__(self, housing_type_id, description, rental_value_month, loan_value_month, bank):
        self.housing_type_id = housing_type_id
        self.description = description
        self.rental_value_month = rental_value_month
        self.loan_value_month = loan_value_month
        self.bank = bank

    def to_dict(self):
        return {
            'housing_type_id': self.housing_type_id,
            'description': self.description,
            'rental_value_month': self.rental_value_month,
            'loan_value_month': self.loan_value_month,
            'bank': self.bank
        }

