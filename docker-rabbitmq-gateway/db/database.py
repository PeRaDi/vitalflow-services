import psycopg2
import os
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        self.conn = None

    async def setup_database(self):
        try:
            config = {
                'host': os.getenv('DATABASE_HOST'),
                'port': os.getenv('DATABASE_PORT'),
                'database': os.getenv('DATABASE_NAME'),
                'user': os.getenv('DATABASE_USERNAME'),
                'password': os.getenv('DATABASE_PASSWORD')
            }
            self.conn = psycopg2.connect(**config)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    async def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def get_connection(self):
        if self.conn is not None:
            return self.conn
        else:
            raise Exception('Database connection not established.')