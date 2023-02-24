import psycopg2
import os

from config import DB_USER, DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
conn.autocommit = True
