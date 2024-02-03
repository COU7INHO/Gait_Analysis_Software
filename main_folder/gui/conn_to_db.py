"""
Database Connection Module

This module provides a function to connect to a PostgreSQL database using the psycopg2 library.
It includes error handling to display a QMessageBox with an error message if the connection fails.

Dependencies:
- psycopg2: For PostgreSQL database interaction.
- PyQt5.QtWidgets: For displaying error messages through QMessageBox.

Functions:
- connect_to_database: Establishes a connection to the PostgreSQL database.

Usage:
- Call the connect_to_database function to obtain a connection and cursor to the PostgreSQL database.
- Ensure the necessary dependencies are installed before using this script.

--------

Query to create PostgreSQL patient's table:

CREATE TABLE patient (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    amputation_level VARCHAR(50) NOT NULL,
    amputated_limb VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    district VARCHAR(50) NOT NULL
);

"""

import psycopg2
from PyQt5.QtWidgets import QMessageBox


def connect_to_database():
    """
    Establish a connection to the PostgreSQL database.

    Returns:
    - conn (psycopg2.extensions.connection): PostgreSQL database connection object.
    - cur (psycopg2.extensions.cursor): PostgreSQL database cursor object.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="admin",
        )
        cur = conn.cursor()
        return conn, cur

    except psycopg2.Error as e:
        # Display an error message using QMessageBox in case of connection failure.
        QMessageBox.critical(None, "Error connecting to database", str(e))
