from config.database import get_connection
from model.cart import Cart

class CartDAO:
    def add_to_cart(self, cart):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO CART(user_id, product_id, quantity) VALUES (%s, %s, %s)
        """

        values  = (
            cart.user_id,
            cart.product_id,
            cart.quantity
            )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

    def get_user_cart(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT c.cart_id, c.user_id, c.product_id, c.quantity, p.product_name, p.price, p.stock 
        FROM cart c INNER JOIN products p
        ON c.product_id = p.product_id
        WHERE c.user_id = %s
        """

        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows

    def get_cart_item(self, user_id, product_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT cart_id, user_id, product_id, quantity
        FROM cart WHERE user_id = %s
        AND product_id = %s
        """

        cursor.execute(query, (user_id, product_id))
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row:
            return Cart(row[0], row[1], row[2], row[3])

        return None

    def update_quantity(self, cart_id, quantity):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE cart SET quantity = %s
        WHERE cart_id = %s
        """

        cursor.execute(query, (quantity, cart_id))
        connection.commit()

        cursor.close()
        connection.close()

    def remove_from_cart(self, cart_id, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        DELETE FROM cart
        WHERE cart_id = %s
        AND user_id = %s
        """

        cursor.execute(query, (cart_id, user_id))
        connection.commit()

        cursor.close()
        connection.close()

    def clear_cart(self,user_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = "DELETE FROM cart WHERE user_id = %s"

        cursor.execute(query, (user_id,))
        connection.commit()

        cursor.close()
        connection.close()


        
