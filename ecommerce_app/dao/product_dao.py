from config.database import get_connection
from model.product import Product

class ProductDAO:
    def get_all_product(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")

        rows = cursor.fetchall()
        products = []

        for row in rows:
            product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
            products.append(product)

        cursor.close()
        connection.close()

        return products
    
    def get_product_by_id(self, product_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM products WHERE product_id = %s"

        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row:
            return Product(row[0], row[1], row[2], row[3], row[4], row[5])

        return None

    def search_products(self, keyword):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT * FROM products
        WHERE product_name LIKE %s
        """

        cursor.execute(query, ("%" + keyword + "%",))

        rows = cursor.fetchall()
        products = []

        for row in rows:
            products.append(Product(row[0],row[1],row[2],row[3],row[4],row[5]))

        cursor.close()
        connection.close()

        return products

    def add_product(self, product):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO products (product_name, price, stock, supplier_id, category_id)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            product.product_name,
            product.price,
            product.stock,
            product.supplier_id,
            product.category_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

    def add_product(self, product_name, price, stock, supplier_id, category_id):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO products
        (product_name, price, stock, supplier_id, category_id)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                product_name,
                price,
                stock,
                supplier_id,
                category_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

    def delete_product(self, product_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = "DELETE FROM products WHERE product_id = %s"

        cursor.execute(query, (product_id,))
        connection.commit()

        cursor.close()
        connection.close()

    def get_products_paginated(self, page=1, page_size=5):

        connection = get_connection()
        cursor = connection.cursor()

        offset = (page - 1) * page_size

        query = """
        SELECT * FROM products
        LIMIT %s OFFSET %s
        """

        cursor.execute(query, (page_size, offset))

        rows = cursor.fetchall()
        products = []

        for row in rows:
            products.append(
                Product(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )

        cursor.close()
        connection.close()

        return products

