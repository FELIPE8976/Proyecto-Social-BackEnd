class Department:
    def __init__(self, department_id, name):
        self.department_id = department_id
        self.name = name

    def to_dict(self):
        return {
            'department_id': self.department_id,
            'name': self.name
        }
