import os

import mysql.connector
from mysql.connector import Error, MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def connect_to_database():
    try:
        return mysql.connector.connect(host=os.getenv('DB_HOST'),
                                       database=os.getenv('DB_DATABASE'),
                                       user=os.getenv('DB_USER'),
                                       password=os.getenv('DB_PASSWORD'),
                                       port=os.getenv('DB_PORT'))

    except Error as e:
        print("Error while connecting to MySQL:", e)


def create_user(username, password_hashed, email) -> None:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user (username, password, email, createBy, updateBy)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, password_hashed, email, username, username))
    conn.commit()
    conn.close()


def get_user_from_db(username: str) -> tuple:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
       SELECT username, password, role FROM user
       WHERE username = %s
   """, (username,))

    row = cursor.fetchone()
    conn.close()
    return row if row else None
