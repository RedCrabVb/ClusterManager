import fnmatch
import json
import logging
import zipfile
from datetime import timedelta, datetime

from jose import JWTError, jwt
import psycopg2.extras
from fastapi import FastAPI, Depends, HTTPException
from psycopg2 import sql
from passlib.context import CryptContext
from starlette import status

import config
from cm.db import *
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
import base64
import shutil
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from cm.service import ServiceTemplate

from cm.base_model import *

import os

InitFilesDir = config.INIT_FILES_DIR
ClusterDir = config.CLUSTER_DIR

origins = [
    config.ORIGINS_WEB_APP,
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
]

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = FastAPI(middleware=middleware)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



wd = os.getcwd()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM user_cm WHERE username = %s', (username,))
        records = cursor.fetchone()

        return UserInDB(username=records['username'], hashed_password=records['hash_password'])


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=config.expire_token)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
    user = get_user(conn, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=int(config.expire_token))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/update_password')
def update_password(new_password: str, current_user: User = Depends(get_current_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE user_cm SET hash_password = %s WHERE username = %s',
                       (get_password_hash(new_password), current_user.username,))
        return {'Status': 'Ok'}


@app.post('/task/test_connection')
def test_connection(host: HostService, current_user: User = Depends(get_current_active_user)):
    return {'Status': host.test_connection()}


@app.post('/task/run_action')
def add_task(runActionModel: RunActionModel, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (runActionModel.cluster_name,))
        records = cursor.fetchone()
        for i_file in json.loads(records['data']):
            if i_file['extid'] == runActionModel.extid_service:
                service_tmp = ServiceTemplate(i_file)
                return {'ProcId': service_tmp.run_action_sh(runActionModel.extid, records['path_cluster_dir'],
                                                            runActionModel.shell_parameters)}


@app.get('/task/status')
def get_status_task(proc_id: int, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('select * from process where id = %s', (proc_id,))
        record = cursor.fetchone()

        return dict(record)


@app.get('/task/statuses')
def get_status_task(current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('select command, extid_action, is_complite, stdout, date_start, code_return, id'
                       ' from process p order by id desc limit 100')
        records = cursor.fetchall()

        return [dict(idx) for idx in records]


@app.get('/hosts')
def list_host(current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM hosts')
        records = cursor.fetchall()

        return [dict(ix) for ix in records]


@app.post('/host/delete')
def delete_host(host: HostService, current_user: User = Depends(get_current_active_user)):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM hosts WHERE hostname = %s and username = %s', (host.hostname, host.username))

    return {'Status': 'Ok'}


@app.post('/host')
def add_host(host: HostService, current_user: User = Depends(get_current_active_user)):
    with conn.cursor() as cursor:
        insert_host = sql.SQL('insert into hosts (hostname, username, password, status_connect) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(host.hostname, host.username, host.password, False)]))
        )
        cursor.execute(insert_host)

    return {'Status': 'Ok'}


@app.get('/cluster')
def list_cluster(current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters')
        records = cursor.fetchall()

        results = [dict(ix) for ix in records]
        for result in results:
            result['data'] = json.loads(result['data'])
            result['item'] = json.loads(result['item'])

    return results


@app.post('/cluster/host/save')
def save_host(name_cluster: str, extid_service: str, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (name_cluster,))
        records = cursor.fetchone()

        for s in json.loads(records['data']):
            if s['extid'] == extid_service:
                service = ServiceTemplate(s)
                service.save_hosts_to_cluster(records['path_cluster_dir'])


@app.post("/cluster/host")
def add_host_to_cluster(itemAddClusterHost: ItemAddClusterHost, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (itemAddClusterHost.name_cluster,))
        records = cursor.fetchone()

        update_data = json.loads(records['data'])
        for s in update_data:
            if s['extid'] == itemAddClusterHost.extid_service:
                service = ServiceTemplate(s)
                service.add_host(itemAddClusterHost.host, itemAddClusterHost.group)

        cursor.execute('UPDATE clusters SET data = %s WHERE name = %s',
                       (json.dumps(update_data), itemAddClusterHost.name_cluster))


@app.get('/cluster/conf/list')
def get_conf_list(cluster_name: str, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (cluster_name,))
        records = cursor.fetchone()

        configs = []
        for (path, dir_names, filenames) in os.walk(records['path_cluster_dir'] + '/vars'):
            for f in filenames:
                with open(records['path_cluster_dir'] + '/vars/' + f) as f_content:
                    configs.append({'filename': f, 'content': f_content.read()})

        return configs

    raise HTTPException(status_code=400, detail='Not found conf')


@app.post('/cluster/delete')
def delete_cluster(clusterName: str, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters WHERE name = %s', (clusterName,))
        records = cursor.fetchone()

        try:
            shutil.rmtree(Path(records['path_cluster_dir']))
        except OSError as e:
            logging.error(f'cluster/delete error delete {e.strerror}')

        cursor.execute('DELETE FROM clusters WHERE name = %s', (clusterName,))

    return {'Status': 'Ok'}


@app.post('/cluster/conf/update')
def update_conf(cluster: ClusterUpdate, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters WHERE name = %s', (cluster.cluster_name,))
        records = cursor.fetchone()

        path_conf = records['path_cluster_dir']
        with open(f'{path_conf}/vars/{cluster.config_name}', 'w') as f_init:
            f_init.write(cluster.config_file)
            return {'Status', 'Ok'}

    raise HTTPException(status_code=400, detail='Not found conf')


@app.post('/cluster')
def create_cluster(cluster: ClusterUser, current_user: User = Depends(get_current_active_user)):
    import zipfile
    import os

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        os.chdir(wd)

        (name_init_file, version_cluster) = cluster.initfile_name.split('|')
        cursor.execute('SELECT * FROM init_files WHERE version = %s AND name = %s', (version_cluster, name_init_file))
        records = cursor.fetchone()

        item_name = records['name']
        item_namefile = records['namefile']
        item_version = records['version']
        path_init_file = Path(f'{InitFilesDir}/{item_name}/{item_namefile}')
        path_cluster_dir = Path(f'{ClusterDir}/{cluster.name}/{item_name}/{item_version}')
        path_cluster_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(path_init_file, 'r') as zip_ref:
            zip_ref.extractall(path_cluster_dir)

        cluster_files = f'{path_cluster_dir}/{next(os.walk(path_cluster_dir))[1][0]}'

        with open(f'{cluster_files}/conf.json') as f:
            data = json.loads(f.read())
            print(data)

        print('cp item.data')

        insert_host = sql.SQL(
            'insert into clusters (name, description, item, data, path_cluster_dir) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(cluster.name, cluster.description, json.dumps(
                {'item_name': item_name, 'item_version': item_version, 'item_namefile': item_namefile}
            ), json.dumps(data), cluster_files)]))
        )
        cursor.execute(insert_host)

    return {'Status': 'Ok'}


@app.post('/initfile/delete')
def delete_initfile(item_init_file: ItemInitFileVersion, current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM init_files WHERE name = %s and version = %s',
                       (item_init_file.name, item_init_file.version))
        record_init_file = cursor.fetchone()

        try:
            shutil.rmtree(Path(f'{InitFilesDir}/{record_init_file["name"]}'))
        except OSError as e:
            logging.error(f'initfile/delete error delete {e.strerror}')

        cursor.execute('DELETE FROM init_files WHERE name = %s and version = %s',
                       (item_init_file.name, item_init_file.version))

    return {'Status': 'Ok'}


@app.get('/initfile')
def list_init_file(current_user: User = Depends(get_current_active_user)):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM init_files')
        records = cursor.fetchall()
        for ix in records:
            print(dict(ix))

        return [dict(ix) for ix in records]


@app.post("/upload/initfile")
def upload(item: ItemInitFile, current_user: User = Depends(get_current_active_user)):
    with conn.cursor() as cursor:
        Path(f'{InitFilesDir}/{item.name}').mkdir(parents=True, exist_ok=True)
        with open(f'{InitFilesDir}/{item.name}/{item.namefile}', 'wb') as f_init_file:
            f_init_file.write(base64.standard_b64decode(item.data))

        version_init_file = None
        with zipfile.ZipFile(f'{InitFilesDir}/{item.name}/{item.namefile}') as z_init_file:
            for filename in z_init_file.namelist():
                if not os.path.isdir(filename) and fnmatch.fnmatch(filename, '*VERSION'):
                    with z_init_file.open(filename) as f:
                        version_init_file = f.read()

        insert_init_files = sql.SQL('insert into init_files (version, namefile, name) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(version_init_file.decode('UTF-8'), item.namefile, item.name)]))
        )
        cursor.execute(insert_init_files)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
