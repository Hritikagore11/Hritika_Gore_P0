from dao.order_dao import OrderDAO
from dao.cart_dao import CartDAO
from invoice.invoice_generator import InvoiceGenerator
from utils.file_handler import FileHandler

class OrderService:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.cart_dao = CartDAO()
        self.invoice_generator = InvoiceGenerator()
        self.file_handler = FileHandler()

    def place_order(self, user_id):
        cart_items = self.cart_dao.get_user_cart(user_id)

        if not cart_items:
            return False, "Your cart is empty"

        total_amount = 0

        for item in cart_items:
            quantity = item[3]
            price = item[5]
            total_amount += quantity * price

        try:
            order_id = self.order_dao.create_order(
                user_id,
                cart_items,
                total_amount
            )

            order_data = {
                "order_id": order_id,
                "user_id": user_id,
                "total_amount": float(total_amount),
                "status": "PLACED"
            }

            self.file_handler.save_order(order_data)

            return True, f"Order placed successfully. Order ID: {order_id}"

        except Exception as e:
            return False, str(e)
        
    def get_order_history(self, user_id):
        return self.order_dao.get_order_history(user_id)

    def generate_invoice(self, order_id, user_id):
        rows = self.order_dao.get_order_for_invoice(
            order_id,
            user_id
        )

        if not rows:
            return False, "Order not found"

        first_row = rows[0]

        order_id = first_row[0]
        order_date = first_row[1]
        total_amount = first_row[2]
        status = first_row[3]
        customer_name = first_row[4]
        email = first_row[5]

        items = []

        for row in rows:

            product_name = row[6]
            quantity = row[7]
            price = row[8]

            items.append(
                (
                    product_name,
                    quantity,
                    price
                )
            )

        file_path = self.invoice_generator.generate_invoice(
            order_id,
            customer_name,
            email,
            order_date,
            status,
            items,
            total_amount
        )

        return True, file_path