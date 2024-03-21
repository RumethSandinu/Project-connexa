import unittest

from blueprints.admin import Admin
from blueprints.customer import Customer
from blueprints.staff import Staff
from blueprints.db_handler import DatabaseHandler


class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        # Set up the database connection for testing
        self.db_handler = DatabaseHandler()
        # Possibly insert test data into the database

    def tearDown(self):
        # Close the database connection after testing
        self.db_handler.close_connection()

    def test_insert_customer(self):
        # Create a customer instance and insert into the database
        customer = Customer("test@example.com", "password123", "John", "Doe", "2000-01-01",
                            "123 Street", "City", "Province", "12345")
        self.assertTrue(self.db_handler.insert_customer(customer))

    def test_insert_staff(self):
        # Create a staff instance and insert into the database
        staff = Staff("staff@connexa.com", "S123", "password123", "Jane", "Smith", "1990-01-01")
        self.assertTrue(self.db_handler.insert_staff(staff))

    def test_insert_admin(self):
        # Create an admin instance and insert into the database
        admin = Admin("admin@connexa.com", "A123")
        self.assertTrue(self.db_handler.insert_admin(admin))

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
