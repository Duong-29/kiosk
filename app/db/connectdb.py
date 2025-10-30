import mysql.connector
from mysql.connector import errorcode
from app.core.config import settings

def connect():
    config = {
        "user": settings.DB_USER,
        "password": settings.DB_PASSWORD,
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_NAME,
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        # conn.database = settings.DB_NAME
        print("DATABASE CONNECTED")
        return conn, cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Sai username || password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("DATABASE NOT EXISTS")
        else:
            print("Error Connect: ", err)
        return None, None
    
def disconnect(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("Disconnected Database")