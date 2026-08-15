from config.database import get_connection

class OrderDAO:
    def create_order(self, user_id, cart_items, total_amount):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            order_query = """
            INSERT INTO orders
            (user_id, order_date, total_amount, status)
            VALUES (%s, NOW(), %s, %s)
            """
            cursor.execute(order_query,(user_id, total_amount, "PLACED"))
            order_id = cursor.lastrowid  #get generated order ID

            detail_query = """
            INSERT INTO order_details
            (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
            """

            stock_query = """                    
            UPDATE products
            SET stock = stock - %s
            WHERE product_id = %s
            AND stock >= %s
            """    #reduces stock

            for item in cart_items:
                product_id = item[2]
                quantity = item[3]
                price = item[5]

                cursor.execute(detail_query,
                    (
                        order_id,
                        product_id,
                        quantity,
                        price
                    )
                )

                cursor.execute(stock_query,
                    (
                        quantity,
                        product_id,
                        quantity
                    )
                )

                if cursor.rowcount == 0:
                    raise Exception("Insufficient stock")

            clear_cart_query = """
            DELETE FROM cart
            WHERE user_id = %s
            """

            cursor.execute(clear_cart_query,(user_id,))

            connection.commit()
            return order_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_order_history(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT  o.order_id, o.order_date, o.total_amount, o.status, p.product_name, od.quantity, od.price
        FROM orders o INNER JOIN order_details od ON o.order_id = od.order_id
        INNER JOIN products p ON od.product_id = p.product_id
        WHERE o.user_id = %s ORDER BY o.order_date DESC
        """

        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        return rows

    def get_order_for_invoice(self, order_id, user_id):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT o.order_id, o.order_date, o.total_amount, o.status, u.name, u.email, p.product_name, od.quantity, od.price
        FROM orders o INNER JOIN users u
        ON o.user_id = u.user_id
        INNER JOIN order_details od
        ON o.order_id = od.order_id
        INNER JOIN products p
        ON od.product_id = p.product_id
        WHERE o.order_id = %s
        AND o.user_id = %s
        """

        cursor.execute(query, (order_id, user_id))
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows

