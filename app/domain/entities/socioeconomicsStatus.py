
class SocioeconomicStatus:
    def __init__(self, socioeconomic_status_id, socioeconomic_status_value):
        self.socioeconomic_status_id = socioeconomic_status_id
        self.socioeconomic_status_value = socioeconomic_status_value

    def to_dict(self):
        return {
            'socioeconomic_status_id': self.socioeconomic_status_id,
            'socioeconomic_status_value': self.socioeconomic_status_value
        }

