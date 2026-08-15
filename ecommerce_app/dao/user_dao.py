from config.database import get_connection
from model.user import User, Admin, Customer

class UserDAO:
    def register_user(self, user):
        connection = get_connection()
        cursor = connection.cursor()

        query = """INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"""

        values = (
            user.name,
            user.email,
            user.password,
            user.role
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

    def get_user_by_email(self, email):
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email = %s"

        cursor.execute(query, (email,))
        row = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if row:
            if row[4] == "ADMIN":
                return Admin(row[0], row[1], row[2], row[3])
            
            return Customer(row[0], row[1], row[2], row[3])
        return None
