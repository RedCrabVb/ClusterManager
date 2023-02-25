import psycopg2

from psycopg2 import sql

from cm.base_model import HostModel
from config import DB_USER, DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
conn.autocommit = True


def db_delete_cluster(name_cluster: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('DELETE FROM clusters WHERE name = %s', (name_cluster,))


def db_get_cluster(name_cluster: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters WHERE name = %s', (name_cluster,))
        record = cursor.fetchone()
        return record


def db_update_cluster(name_cluster: str, name_field: str, value_field: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'UPDATE clusters SET {name_field} = %s WHERE name = %s',
                       # (json.dumps(update_data), itemAddClusterHost.name_cluster))
                       (value_field, name_cluster))


def db_delete_host(hostname, username):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM hosts WHERE hostname = %s and username = %s', (hostname, username))


def db_insert_host(host: HostModel):
    with conn.cursor() as cursor:
        insert_host = sql.SQL('insert into hosts (hostname, username, password, status_connect, private_key) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(host.hostname, host.username, host.password, False, host.private_key)]))
        )
        cursor.execute(insert_host)


def db_get_status_task(limit: int):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('select command, extid_action, is_complite, stdout, date_start, code_return, id'
                       ' from process p order by id desc limit %s', (limit,))
        records = cursor.fetchall()

        return [dict(idx) for idx in records]


def db_get_hosts():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM hosts')
        records = cursor.fetchall()

        return [dict(ix) for ix in records]


def db_get_process(proc_id: int):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('select * from process where id = %s', (proc_id,))
        record = cursor.fetchone()

        return dict(record)


def db_update_password(hash_password: str, username: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE user_cm SET hash_password = %s WHERE username = %s',
                       (hash_password, username))


def db_insert_init_files(version: str, license_text: str, namefile: str, name: str):
    with conn.cursor() as cursor:
        insert_init_files = sql.SQL('insert into init_files (version, license_text, namefile, name) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(version, license_text, namefile, name)]))
        )
        cursor.execute(insert_init_files)


def db_update_init_file(name: str, version: str):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE init_files SET license = true WHERE name = %s and version = %s',
                       (name, version))


def db_get_all_init_files():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM init_files')
        return cursor.fetchall()


def db_delete_init_files(name: str, version: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('DELETE FROM init_files WHERE name = %s and version = %s',
                       (name, version))


def db_get_init_files(name: str, version: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM init_files WHERE version = %s AND name = %s', (version, name))
        record = cursor.fetchone()
        return record


def db_insert_clusters(name: str, description: str, item: str, data: str, path_cluster_dir: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        insert_host = sql.SQL(
            'insert into clusters (name, description, item, data, path_cluster_dir) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(name, description, item, data, path_cluster_dir)]))
        )
        cursor.execute(insert_host)
