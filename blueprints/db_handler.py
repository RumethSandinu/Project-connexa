import hashlib
import secrets

import mysql.connector

class DatabaseHandler:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',  # replace with your MySQL server host
                user='root',  # replace with your MySQL username
                password='',  # replace with your MySQL password
                database='connexa'  # replace with your MySQL database name
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_customer(self, customer):
        customer_data = (customer.email, customer.password, customer.f_name, customer.l_name, customer.dob,
                         customer.street, customer.city, customer.province, customer.postal_code)

        try:
            self.cursor.execute('''
                INSERT INTO customer (email, f_name, l_name, dob, user_password, street, city, province, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', customer_data)
            self.conn.commit()
            return True  # Success
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Failure

    def insert_staff(self, staff):
        staff_data = (staff.email, staff.staff_id, staff.password, staff.f_name, staff.l_name, staff.dob)

        try:
            self.cursor.execute('''
                INSERT INTO staff VALUES (%s, %s, %s, %s, %s, %s)
            ''', staff_data)
            self.conn.commit()
            return True  # Success
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Failure

    def insert_admin(self, admin):
        admin_data = (admin.email, admin.admin_id)

        try:
            self.cursor.execute('''
                INSERT INTO admin VALUES (%s, %s)
            ''', admin_data)
            self.conn.commit()
            return True  # Success
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Failure

    def insert_user_contact(self, email, contact):
        user_contact_data = (email, contact)

        try:
            self.cursor.execute('''
                INSERT INTO User_contact VALUES (%s, %s)
            ''', user_contact_data)
            self.conn.commit()
            return True  # Success
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Failure

    def authenticate_customer(self, email, password):
        customer_data = self.get_customer_by_email(email, password)

        print("Customer Data:", customer_data)
        return customer_data


    def get_customer_email(self):
        return self.email

    def authenticate_staff(self, email, password):
        staff_data = self.get_staff_by_email(email, password)

        print("Staff Data:", staff_data)
        return staff_data


    def authenticate_admin(self, email, password):
        admin_data = self.get_admin_by_email(email)

        if admin_data and self.verify_password(password, admin_data[1], admin_data[2]):
            return admin_data
        else:
            return None

    def verify_password(self, input_password, hashed_password, salt):
        input_password_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), salt, 128)
        return hashed_password == input_password_hash

    def hash_password(self, password):
        salt = secrets.token_bytes(16)  # Generate a random salt
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 128)
        return password_hash, salt

    def get_customer_by_email(self, email, password):
        self.cursor.execute('SELECT email, user_password FROM customer WHERE email = %s AND user_password = %s', (email, password))
        customer_data = self.cursor.fetchone()
        if customer_data is None:
            print("You cannot login there is no you data")
        else:
            return customer_data

    def get_staff_by_email(self, email, password):
        self.cursor.execute('SELECT email, user_password FROM staff WHERE email = %s AND user_password = %s', (email, password))
        staff_data = self.cursor.fetchone()
        if staff_data is None:
            print("you cannot login there is no your data here")
        else:
            return staff_data

    def get_admin_by_email(self, email):
        self.cursor.execute('SELECT email, password FROM admin WHERE email = %s', (email,))
        admin_data = self.cursor.fetchone()
        return admin_data

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
