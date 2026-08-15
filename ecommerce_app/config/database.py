import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Rutu1234@",
        database="ecommerce_db"
    )
    return connection

connect = get_connection()
