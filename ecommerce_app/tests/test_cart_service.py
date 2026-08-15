from unittest.mock import MagicMock
from service.cart_service import CartService

def test_add_to_cart():
    service = CartService()

    service.cart_dao = MagicMock()
    service.product_dao = MagicMock()

    product = MagicMock()
    product.stock = 10

    service.product_dao.get_product_by_id.return_value = product
    service.cart_dao.get_cart_item.return_value = None
    service.cart_dao.add_to_cart.return_value = True

    success, message = service.add_to_cart(
        2,
        1,
        2
    )

    assert success is True

def test_empty_cart():
    service = CartService()
    service.cart_dao = MagicMock()

    service.cart_dao.get_user_cart.return_value = []

    cart = service.view_cart(2)

    assert cart == []