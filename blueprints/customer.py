from blueprints.user import User


class Customer(User):
    def __init__(self, email, password, f_name, l_name, dob, street, city, province, postal_code):
        super().__init__(email, password, f_name, l_name, dob)
        self.street = street
        self.city = city
        self.province = province
        self.postal_code = postal_code
