import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load database details from the .env file
load_dotenv()


class DatabaseConnection:

    # Singleton instance
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

        return cls._instance

    # Connect to MySQL database
    def get_connection(self):

        try:
            if self._connection is None or not self._connection.is_connected():

                self._connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "oltp_db"),
                use_pure=True
                )

                print("Database connected successfully!")

            return self._connection

        except Error as e:
            print("Database connection error:", e)
            return None

    # Close database connection
    def close_connection(self):

        if self._connection is not None and self._connection.is_connected():

            self._connection.close()
            self._connection = None

            print("Database connection closed.")