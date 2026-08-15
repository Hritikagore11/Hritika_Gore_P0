from dao.cart_dao import CartDAO
from dao.product_dao import ProductDAO
from model.cart import Cart

class CartService:
    def __init__(self):
        self.cart_dao = CartDAO()
        self.product_dao = ProductDAO()

    def add_to_cart(self, user_id, product_id, quantity):
        if quantity <= 0:
            return False, "Quantity must be greater than 0"

        product = self.product_dao.get_product_by_id(product_id)

        if product is None:
            return False, "Product not found"

        existing_cart = self.cart_dao.get_cart_item(user_id,product_id)

        if existing_cart:
            new_quantity = existing_cart.quantity + quantity
            if new_quantity > product.stock:
                return False, "Insufficient stock"

            self.cart_dao.update_quantity(existing_cart.cart_id,new_quantity)
            return True, "Cart quantity updated"

        if quantity > product.stock:
            return False, "Insufficient stock"

        cart = Cart(0, user_id, product_id, quantity)
        self.cart_dao.add_to_cart(cart)

        return True, "Product added to cart"

    def view_cart(self, user_id):
        return self.cart_dao.get_user_cart(user_id)

    def remove_from_cart(self, cart_id, user_id):
        deleted = self.cart_dao.remove_from_cart(cart_id, user_id)

        if deleted == 0:
            return False, "Cart item not found"

        return True, "Product removed from cart"


