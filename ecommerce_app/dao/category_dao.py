from config.database import get_connection
from model.category import Category

class CategoryDAO:
    def add_category(self, category):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO categories (category_name)
        VALUES (%s)
        """

        cursor.execute(query, (category.category_name,))
        connection.commit()

        cursor.close()
        connection.close()

    def get_all_categories(self):
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM categories"

        cursor.execute(query)
        rows = cursor.fetchall()

        categories = []

        for row in rows:
            category = Category(row[0], row[1])
            categories.append(category)

        cursor.close()
        connection.close()

        return categories

    def get_category_by_id(self, category_id):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT * FROM categories
        WHERE category_id = %s
        """

        cursor.execute(query, (category_id,))
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row:
            return Category(row[0], row[1])

        return None