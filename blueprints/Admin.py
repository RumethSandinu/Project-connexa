from blueprints.User import User


class Admin(User):
    def __init__(self, email, admin_id):
        super().__init__(email, "", "", "", "")  # Admin doesn't need password, name, or dob
        self.admin_id = admin_id