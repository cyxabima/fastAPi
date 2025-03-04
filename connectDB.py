import psycopg
import time

# from psycopg.rows import dict_row


def db_connect():
    while True:
        DB_NAME = "fastapi"
        DB_USER = "postgres"
        DB_PASSWORD = "123Ukasha@"
        DB_HOST = "localhost"
        DB_PORT = 5432  # Default PostgreSQL port
        try:
            # Create a connection
            conn = psycopg.connect(
                f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}",
                row_factory=psycopg.rows.dict_row,
            )
            #   Create a cursor
            cur = conn.cursor()
            print("DATA BASE CONNECTED SUCCESSFULLY")

            return conn, cur
        except Exception as error:
            print("failed connection")
            print(error)
            time.sleep(2)
