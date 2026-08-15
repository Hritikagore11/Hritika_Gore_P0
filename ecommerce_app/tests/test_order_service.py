from unittest.mock import MagicMock
from service.order_service import OrderService

def test_empty_cart():
    service = OrderService()

    service.order_dao = MagicMock()
    service.cart_dao = MagicMock()
    service.file_handler = MagicMock()

    service.cart_dao.get_user_cart.return_value = []

    success, message = service.place_order(2)

    assert success is False
    assert message == "Your cart is empty"


def test_place_order():
    service = OrderService()

    service.order_dao = MagicMock()
    service.cart_dao = MagicMock()
    service.file_handler = MagicMock()

    cart_items = [
        (
            1,
            2,
            1,
            2,
            "Dell Laptop",
            55000
        )
    ]

    service.cart_dao.get_user_cart.return_value = cart_items
    service.order_dao.create_order.return_value = 1

    success, message = service.place_order(2)

    assert success is True
    assert "Order placed successfully" in message


def test_insufficient_stock():
    service = OrderService()

    service.order_dao = MagicMock()
    service.cart_dao = MagicMock()
    service.file_handler = MagicMock()

    cart_items = [
        (
            1,
            2,
            1,
            100,
            "Dell Laptop",
            55000
        )
    ]

    service.cart_dao.get_user_cart.return_value = cart_items

    service.order_dao.create_order.side_effect = Exception(
        "Insufficient stock"
    )

    success, message = service.place_order(2)

    assert success is False
    assert message == "Insufficient stock"