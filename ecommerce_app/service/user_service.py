from dao.user_dao import UserDAO
from model.user import Customer
import hashlib

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, name, email, password):
        if not name.strip():
            return False, "Name cannot be empty"

        if not email.strip():
            return False, "Email cannot be empty"

        if not password.strip():
            return False, "Password cannot be empty"

        existing_user = self.user_dao.get_user_by_email(email)

        if existing_user:
            return False, "Email already registered"

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        user = Customer(1, name, email, hashed_password)

        self.user_dao.register_user(user)
        return True, "Registration successful"

    def login(self, email, password):
        user = self.user_dao.get_user_by_email(email)

        if user is None:
            return None, "Invalid email or password"

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        if hashed_password != user.password:
            return None, "Invalid email or password"

        return user, "Login successful"

        