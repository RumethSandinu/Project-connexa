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
        # Retrieve the hashed password and salt from the database for the given email
        self.cursor.execute('SELECT email, user_password FROM customer WHERE email = %s', (email,))
        print("DB", email, password)
        customer_data = self.cursor.fetchone()
        print("hi", customer_data)

        if customer_data:
            email_db, hashed_password_db = customer_data
            print(customer_data)
            print(password)
            print(hashed_password_db)
            hashed_password_input = password
            print(hashed_password_input)
            # Compare the hashed input password with the hashed password retrieved from the database
            if hashed_password_input == hashed_password_db:
                print("sucess")
                return email_db  # Authentication successful
            else:
                print("fail")
                return None  # Authentication failed
        else:
            print("user no")
        return None  # User not found

    def authenticate_staff(self, email, password):
        # Retrieve the hashed password and salt from the database for the given email
        self.cursor.execute('SELECT email, user_password FROM staff WHERE email = %s', (email,))
        staff_data = self.cursor.fetchone()

        if staff_data:
            email_db, hashed_password_db= staff_data
            hashed_password_input = password
            print(hashed_password_input)
            # Compare the hashed input password with the hashed password retrieved from the database
            if hashed_password_input == hashed_password_db:
                print("sucess")
                return email_db  # Authentication successful
            else:
                print("fail")
                return None  # Authentication failed
        else:
            print("user no")
        return None  # User not found

    def authenticate_admin(self, email, password):
        # Retrieve the hashed password and salt from the database for the given email
        self.cursor.execute('SELECT email, password, salt FROM admin WHERE email = %s', (email,password))
        admin_data = self.cursor.fetchone()

        if admin_data:
            email_db, hashed_password_db = admin_data
            hashed_password_input = password
            print(hashed_password_input)
            # Compare the hashed input password with the hashed password retrieved from the database
            if hashed_password_input == hashed_password_db:
                print("sucess")
                return email_db  # Authentication successful
            else:
                print("fail")
                return None  # Authentication failed
        else:
            print("user no")
        return None  # User not found

    def verify_password(self, input_password, hashed_password):
        input_password_hash = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
        return input_password_hash == hashed_password

    def hash_password(self, password):
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return password_hash

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
