# test_signup.py
import unittest
from unittest.mock import patch
from signup import signup
import sqlite3
import hashlib

class TestSignup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary in-memory SQLite database for testing
        cls.conn = sqlite3.connect('app_database.db')
        cls.c = cls.conn.cursor()
        # Create a user table
        cls.c.execute('''CREATE TABLE User (EmployeeID TEXT PRIMARY KEY, Name TEXT, Email TEXT, Password TEXT)''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        # Close the connection and clean up
        cls.conn.close()

    @patch('tkinter.messagebox.showinfo')
    def test_signup_success(self, mock_showinfo):
        # Test a successful signup attempt
        employee_id = "7"
        name = "Logine Magdy"
        email = "loginemagdy777@gmail.com"
        password = "Password@1"
        confirm_password = "Password@1"
        result = signup(employee_id, name, email, password, confirm_password)
        self.assertEqual(result, "Success")
        mock_showinfo.assert_called_once()

        # Verify that the user was added to the database with the hashed password
        self.c.execute("SELECT * FROM User WHERE EmployeeID=?", (employee_id,))
        user = self.c.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[2], email)
        self.assertEqual(user[3], hashlib.md5(password.encode()).hexdigest())

    @patch('tkinter.messagebox.showerror')
    def test_signup_password_mismatch(self, mock_showerror):
        # Test a signup attempt with password mismatch
        employee_id = "12"
        name = "John Doe"
        email = "johndoe@example.com"
        password = "Password@1"
        confirm_password = "Password@2"  # Mismatched password
        result = signup(employee_id, name, email, password, confirm_password)
        self.assertEqual(result, "Password and Confirm password did not match!!")
        mock_showerror.assert_called_once()

    # Add more test cases for other scenarios (missing fields, invalid email, etc.)

if __name__ == '__main__':
    unittest.main()
