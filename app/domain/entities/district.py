
class District:
    def __init__(self, district_id, district_name):
        self.district_id = district_id
        self.district_name = district_name

    def to_dict(self):
        return {
            'district_id': self.district_id,
            'district_name': self.district_name
        }

