import psycopg2

conn = psycopg2.connect(dbname='cm', user='cm_user',
                        password='pass', host='localhost', port='34543')
conn.autocommit = True
