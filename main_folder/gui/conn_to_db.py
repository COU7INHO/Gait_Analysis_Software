import psycopg2
from PyQt5.QtWidgets import QMessageBox


def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="admin",
        )
        cur = conn.cursor()
        return conn, cur

    except psycopg2.Error as e:
        QMessageBox.critical("Error connecting to database:", e)
