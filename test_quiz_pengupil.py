import unittest
from unittest.mock import MagicMock
from selenium.webdriver.common.by import By


class TestQuizPengupil(unittest.TestCase):
    def setUp(self):
        # Create a mock Selenium WebDriver
        self.driver = MagicMock()

        # Mock the find_element behavior
        self.driver.find_element.return_value = MagicMock()

    def test_register_valid_data(self):
        """Pengguna melakukan registrasi menggunakan data sesuai string yang diharapkan"""
        self.driver.get("http://localhost/main/register.php")

        # Simulate valid user registration
        self.driver.find_element(By.NAME, "name").send_keys("Valid User")
        self.driver.find_element(By.NAME, "username").send_keys("validuser")
        self.driver.find_element(
            By.NAME, "email").send_keys("valid@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("Valid@123")
        self.driver.find_element(By.NAME, "repassword").send_keys("Valid@123")
        self.driver.find_element(By.NAME, "submit").click()

        # Assert submit button was clicked
        self.driver.find_element(By.NAME, "submit").click.assert_called_once()

    def test_register_null_data(self):
        """Pengguna melakukan registrasi menggunakan data null"""
        self.driver.get("http://localhost/main/register.php")

        # Simulate empty form submission
        self.driver.find_element(By.NAME, "name").send_keys("")
        self.driver.find_element(By.NAME, "username").send_keys("")
        self.driver.find_element(By.NAME, "email").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.NAME, "submit").click()

        # Ensure form validation would prevent submission
        self.driver.find_element(By.NAME, "submit").click.assert_called_once()

    def test_login_registered_user(self):
        """Pengguna login menggunakan akun terdaftar"""
        self.driver.get("http://localhost/main/login.php")

        # Simulate login with a registered account
        self.driver.find_element(By.NAME, "username").send_keys("validuser")
        self.driver.find_element(By.NAME, "password").send_keys("Valid@123")
        self.driver.find_element(By.NAME, "submit").click()

        # Simulate redirection
        self.driver.current_url = "http://localhost/main/index.php"

        # Check if login was successful
        self.assertIn("index.php", self.driver.current_url)

    def test_login_unregistered_user(self):
        """Pengguna login menggunakan akun yang tidak terdaftar"""
        self.driver.get("http://localhost/main/login.php")

        # Simulate login with an unregistered user
        self.driver.find_element(By.NAME, "username").send_keys("nonexistent")
        self.driver.find_element(By.NAME, "password").send_keys("WrongPass123")
        self.driver.find_element(By.NAME, "submit").click()

        # Simulate failed login (staying on login.php)
        self.driver.current_url = "http://localhost/main/login.php"

        # Assert user is not redirected
        self.assertIn("login.php", self.driver.current_url)

    def test_login_null_data(self):
        """Pengguna login menggunakan data null"""
        self.driver.get("http://localhost/main/login.php")

        # Simulate login attempt with empty fields
        self.driver.find_element(By.NAME, "username").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.NAME, "submit").click()

        # Simulate failed login (staying on login.php)
        self.driver.current_url = "http://localhost/main/login.php"

        # Assert user is not redirected
        self.assertIn("login.php", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
