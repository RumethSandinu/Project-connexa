import unittest

from blueprints.user import User


class TestUser(unittest.TestCase):
    def test_set_password(self):
        user = User("test@example.com", "password123", "John", "Doe", "2000-01-01")
        self.assertTrue(user.verify_password("password123"))
if __name__ == '__main__':
    unittest.main()