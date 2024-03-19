import hashlib
import os
import bcrypt

class User:
    def __init__(self, email, password, f_name, l_name, dob):
        self.email = email
        self.set_password(password)
        self.f_name = f_name
        self.l_name = l_name
        self.dob = dob

    def set_password(self, password):
        # Use hashlib to securely hash the password
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1000)
        self.password = key + salt

    def verify_password(self, input_password):
        input_password_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), self.password[32:], 1000)
        return self.password[:32] == input_password_hash

    # --------------------------------------------------------------------
    # hashing using bcrypt algorithm
    def set_bcrypt_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_bcrypt_password(self, input_password):
        return bcrypt.checkpw(input_password.encode('utf-8'), self.password_hash)