from blueprints.User import User


class Staff(User):
    def __init__(self, email, staff_id, password, f_name, l_name, dob):
        super().__init__(email, password, f_name, l_name, dob)
        self.staff_id = staff_id