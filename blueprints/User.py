import hashlib
import os

class User:
    def __init__(self, email, password, f_name, l_name, dob):
        self.email = email
        self.set_password(password)
        self.f_name = f_name
        self.l_name = l_name
        self.dob = dob
