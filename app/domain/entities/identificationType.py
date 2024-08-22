

class IdentificationType:
    def __init__(self, identification_type_id, description):
        self.identification_type_id = identification_type_id
        self.description = description

    def to_dict(self):
        return {
            'identification_type_id': self.identification_type_id,
            'description': self.description
        }

