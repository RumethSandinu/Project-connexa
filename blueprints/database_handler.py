import hashlib

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
                INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        customer_data = self.get_customer_by_email(email)

        print("Customer Data:", customer_data)

        if customer_data and len(customer_data) >= 3:
            if self.verify_password(password, customer_data[1], customer_data[2]):
                return customer_data
            else:
                return None

    def authenticate_staff(self, email, password):
        staff_data = self.get_staff_by_email(email)

        if staff_data and self.verify_password(password, staff_data[1], staff_data[2]):
            return staff_data
        else:
            return None

    def authenticate_admin(self, email, password):
        admin_data = self.get_admin_by_email(email)

        if admin_data and self.verify_password(password, admin_data[1], admin_data[2]):
            return admin_data
        else:
            return None

    def verify_password(self, input_password, hashed_password, salt):
        input_password_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), salt, 100000)
        return hashed_password == input_password_hash

    def get_customer_by_email(self, email):
        self.cursor.execute('SELECT email, user_password FROM customer WHERE email = %s', (email,))
        customer_data = self.cursor.fetchone()
        return customer_data

    def get_staff_by_email(self, email):
        self.cursor.execute('SELECT email, user_password FROM staff WHERE email = %s', (email,))
        staff_data = self.cursor.fetchone()
        return staff_data

    def get_admin_by_email(self, email):
        self.cursor.execute('SELECT email, password FROM admin WHERE email = %s', (email,))
        admin_data = self.cursor.fetchone()
        return admin_data

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
