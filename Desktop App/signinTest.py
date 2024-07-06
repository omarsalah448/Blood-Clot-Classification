import unittest
from unittest.mock import patch
from signin import login, hash_password

class TestLogin(unittest.TestCase):
    @patch('signin.sqlite3.connect')
    @patch('signin.send_email')
    @patch('signin.subprocess.run')
    @patch('signin.messagebox.showinfo')
    def test_login_success(self, mock_showinfo,mock_connect):
        # Mock the database connection and other dependencies
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = ('habibaelmazahy20@gmail.com', hash_password('Habiba'))

    # Call the login function with valid credentials
        result = login('habibaelmazahy20@gmail.com', 'Habiba')

    # Check if the login was successful
        self.assertEqual(result, "incorrect id or password")

    # Check if the appropriate functions were called
        mock_showinfo.assert_called_once()
     


    @patch('signin.sqlite3.connect')
    @patch('signin.send_email')
    @patch('signin.subprocess.run')
    @patch('signin.messagebox.showinfo')
    def test_login_incorrect_password(self, mock_showerror, mock_connect):
        # Mock the database connection and other dependencies
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = ('test@example.com', hash_password('password123'))

        # Call the login function with incorrect password
        result = login('test@example.com', 'wrongpassword')

        # Check if the login failed due to incorrect password
        self.assertEqual(result, "Incorrect email or password!")

        # Check if the appropriate error message was displayed
        mock_showerror.assert_called_once()

   

if __name__ == '__main__':
    unittest.main()

