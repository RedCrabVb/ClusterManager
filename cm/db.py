import psycopg2
import os

conn = psycopg2.connect(dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'],
                        password=os.environ['DB_PASSWORD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT'])
conn.autocommit = True
