# import os


# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'root'
#     MYSQL_PASSWORD = ''
#     MYSQL_DB = 'delivery_dispatch'
#     MYSQL_PORT = 3306



import mysql.connector
from mysql.connector import Error
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'delivery_dispatch'
    MYSQL_PORT = 3306


def check_db_connection():
    try:
        # Establish connection using the configuration from Config class
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        
        if connection.is_connected():
            print("Connection to the database was successful!")
            return True
        else:
            print("Failed to connect to the database.")
            return False

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False

    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")


# Check if the connection is successful
if check_db_connection():
    print("Database is connected!")
else:
    print("Database connection failed!")
