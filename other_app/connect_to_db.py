import psycopg2

def connect_to_database():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='admin'
    )   
    cur = conn.cursor()
    return conn, cur
        