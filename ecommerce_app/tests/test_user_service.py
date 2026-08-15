from unittest.mock import MagicMock
from service.user_service import UserService
import hashlib

def test_valid_login():
    service = UserService()
    service.user_dao = MagicMock()

    mock_user = MagicMock()
    mock_user.email = "user@gmail.com"
    mock_user.password = hashlib.sha256(
    "user123".encode()
    ).hexdigest()

    service.user_dao.get_user_by_email.return_value = mock_user

    user, message = service.login(
        "user@gmail.com",
        "user123"
    )

    assert user is not None
    assert message == "Login successful"


def test_invalid_login():
    service = UserService()
    service.user_dao = MagicMock()

    service.user_dao.get_user_by_email.return_value = None

    user, message = service.login(
        "wrong@gmail.com",
        "wrong123"
    )

    assert user is None
    assert message == "Invalid email or password"