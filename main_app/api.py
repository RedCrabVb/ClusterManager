import fnmatch
import io
import json
import logging
import zipfile
from datetime import timedelta

import psycopg2.extras
from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from starlette.responses import FileResponse, StreamingResponse

import config
from db import *
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
import base64
import shutil
from pathlib import Path
from fastapi.security import OAuth2PasswordRequestForm

from service import ServiceTemplate, authenticate_user, create_access_token, get_current_user, get_password_hash, \
    get_current_active_user, HostService

from base_model import *

import os

InitFilesDir = config.INIT_FILES_DIR
PrototypeInitFilesDir = config.PROTOTYPE_INIT_FILES_DIR
ClusterDir = config.CLUSTER_DIR

origins = [
    config.ORIGINS_WEB_APP,
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

logging.basicConfig(filename=config.record_filename_log, level=config.level_log,
                    format=config.formate_log)

app = FastAPI(middleware=middleware)

wd = os.getcwd()


@app.post("/token", response_model=TokenModel)
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
def update_password(new_password: str, current_user: UserModel = Depends(get_current_user)):
    db_update_password(get_password_hash(new_password), current_user.username)
    return {'Status': 'Ok'}


@app.post('/task/test_connection')
def test_connection(host: HostModel, current_user: UserModel = Depends(get_current_active_user)):
    return {'Status': HostService(host.hostname, host.username, host.password, host.private_key).test_connection()}


@app.post('/task/run_action')
def add_task(runActionModel: RunActionModel, current_user: UserModel = Depends(get_current_active_user)):
    record = db_get_cluster(runActionModel.cluster_name)
    for i_file in json.loads(record['data']):
        if i_file['extid'] == runActionModel.extid_service:
            service_tmp = ServiceTemplate(i_file)
            return {'ProcId': service_tmp.run_action_sh(runActionModel.extid, record['path_cluster_dir'],
                                                        runActionModel.shell_parameters)}


@app.get('/task/status')
def get_status_task(proc_id: int, current_user: UserModel = Depends(get_current_active_user)):
    return db_get_process(proc_id)


@app.get('/task/statuses')
def get_status_task(current_user: UserModel = Depends(get_current_active_user)):
    return db_get_status_task(100)


@app.get('/hosts')
def list_host(current_user: UserModel = Depends(get_current_active_user)):
    return db_get_hosts()


@app.post('/host/delete')
def delete_host(host: HostModel, current_user: UserModel = Depends(get_current_active_user)):
    db_delete_host(host.hostname, host.username)

    return {'Status': 'Ok'}


@app.post('/host')
def add_host(host: HostModel, current_user: UserModel = Depends(get_current_active_user)):
    db_insert_host(host)

    return {'Status': 'Ok'}


def db_get_clusters():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters')
        records = cursor.fetchall()
        return records


@app.get('/cluster')
def list_cluster(current_user: UserModel = Depends(get_current_active_user)):
    results = [dict(ix) for ix in db_get_clusters()]
    for result in results:
        result['data'] = json.loads(result['data'])
        result['item'] = json.loads(result['item'])

    return results


@app.post('/cluster/host/save')
def save_host(name_cluster: str, extid_service: str, current_user: UserModel = Depends(get_current_active_user)):
    record = db_get_cluster(name_cluster)

    for s in json.loads(record['data']):
        if s['extid'] == extid_service:
            service = ServiceTemplate(s)
            service.save_hosts_to_cluster(record['path_cluster_dir'])


@app.post("/cluster/host")
def add_host_to_cluster(itemAddClusterHost: ItemAddClusterHost,
                        current_user: UserModel = Depends(get_current_active_user)):
    record = db_get_cluster(itemAddClusterHost.name_cluster)

    update_data = json.loads(record['data'])
    for s in update_data:
        if s['extid'] == itemAddClusterHost.extid_service:
            service = ServiceTemplate(s)
            service.add_host(itemAddClusterHost.host, itemAddClusterHost.group)

    db_update_cluster(itemAddClusterHost.name_cluster, 'data', json.dumps(update_data))


@app.get('/cluster/conf/list')
def get_conf_list(cluster_name: str, current_user: UserModel = Depends(get_current_active_user)):
    record = db_get_cluster(cluster_name)

    configs = []
    for (path, dir_names, filenames) in os.walk(record['path_cluster_dir'] + '/vars'):
        for f in filenames:
            with open(record['path_cluster_dir'] + '/vars/' + f) as f_content:
                configs.append({'filename': f, 'content': f_content.read()})

        return configs


@app.post('/cluster/delete')
def delete_cluster(clusterName: str, current_user: UserModel = Depends(get_current_active_user)):
    record = db_get_cluster(clusterName)

    try:
        shutil.rmtree(Path(record['path_cluster_dir']))
    except OSError as e:
        logging.error(f'cluster/delete error delete {e.strerror}')

    db_delete_cluster(clusterName)

    return {'Status': 'Ok'}


@app.post('/cluster/conf/update')
def update_conf(cluster: ClusterUpdateModel, current_user: UserModel = Depends(get_current_active_user)):
    record = db_get_cluster(cluster.cluster_name)

    path_conf = record['path_cluster_dir']
    with open(f'{path_conf}/vars/{cluster.config_name}', 'w') as f_init:
        f_init.write(cluster.config_file)
        return {'Status', 'Ok'}


@app.post('/cluster')
def create_cluster(cluster: ClusterUserModel, current_user: UserModel = Depends(get_current_active_user)):
    import zipfile

    os.chdir(wd)

    (name_init_file, version_cluster) = cluster.initfile_name.split('|')
    record = db_get_init_files(name_init_file, version_cluster)

    item_name = record['name']
    item_namefile = record['namefile']
    item_version = record['version']
    path_init_file = Path(f'{InitFilesDir}/{item_name}/{item_namefile}')
    path_cluster_dir = Path(f'{ClusterDir}/{cluster.name}/{item_name}/{item_version}')
    path_cluster_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(path_init_file, 'r') as zip_ref:
        zip_ref.extractall(path_cluster_dir)

    cluster_files = f'{path_cluster_dir}/{next(os.walk(path_cluster_dir))[1][0]}'

    with open(f'{cluster_files}/conf.json') as f:
        data = json.loads(f.read())
        logging.debug(f'Data cluster ({cluster.name}) config: {data}')

    db_insert_clusters(cluster.name, cluster.description, json.dumps(
        {'item_name': item_name, 'item_version': item_version, 'item_namefile': item_namefile}
    ), json.dumps(data), cluster_files)

    return {'Status': 'Ok'}


@app.post('/initfile/delete')
def delete_initfile(item_init_file: ItemInitFileVersion, current_user: UserModel = Depends(get_current_active_user)):
    record_init_file = db_get_init_files(item_init_file.name, item_init_file.version)

    try:
        shutil.rmtree(Path(f'{InitFilesDir}/{record_init_file["name"]}'))
    except OSError as e:
        logging.error(f'initfile/delete error delete {e.strerror}')

    db_delete_init_files(item_init_file.name, item_init_file.version)

    return {'Status': 'Ok'}


@app.get('/initfile')
def list_init_file(current_user: UserModel = Depends(get_current_active_user)):
    records = db_get_all_init_files()
    return [dict(ix) for ix in records]


@app.post('/initfile/accept')
def accept_license_initfile(initfile: ItemInitFileVersion, current_user: UserModel = Depends(get_current_active_user)):
    db_update_init_file(initfile.name, initfile.version)
    return {'Status': 'Ok'}


@app.post("/upload/initfile")
def upload(item: ItemInitFile, current_user: UserModel = Depends(get_current_active_user)):
    Path(f'{InitFilesDir}/{item.name}').mkdir(parents=True, exist_ok=True)
    with open(f'{InitFilesDir}/{item.name}/{item.namefile}', 'wb') as f_init_file:
        f_init_file.write(base64.standard_b64decode(item.data))

    version_init_file = None
    license_text_init_file = None
    with zipfile.ZipFile(f'{InitFilesDir}/{item.name}/{item.namefile}') as z_init_file:
        for filename in z_init_file.namelist():
            if not os.path.isdir(filename) and fnmatch.fnmatch(filename, '*VERSION'):
                with z_init_file.open(filename) as f:
                    version_init_file = f.read()
            if not os.path.isdir(filename) and fnmatch.fnmatch(filename, '*LICENSE'):
                with z_init_file.open(filename) as f:
                    license_text_init_file = f.read()

    db_insert_init_files(version_init_file.decode('UTF-8'), license_text_init_file.decode('UTF-8'),
                         item.namefile, item.name)


@app.get('/initfile/prototype')
def create_initfile_on_prototype(name: str, version: str, path: str,
                                 current_user: UserModel = Depends(get_current_active_user)):
    initfile = db_get_init_files(name, version)
    pathToInitfile = f'{InitFilesDir}/{name}/{initfile["namefile"]}'
    pathExtractPrototypeInitfile = f'{PrototypeInitFilesDir}/{name}/{version}'

    if not Path(pathExtractPrototypeInitfile).exists():
        Path(pathExtractPrototypeInitfile).mkdir(parents=True)
        with zipfile.ZipFile(pathToInitfile, 'r') as zip_ref:
            zip_ref.extractall(pathExtractPrototypeInitfile)

    def path_to_dict(path):
        d = {'name': os.path.basename(path)}
        if os.path.isdir(path):
            d['type'] = "directory"
            d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
        else:
            d['type'] = "file"
        return d

    return path_to_dict(f'{pathExtractPrototypeInitfile}/{path}')


@app.get('/initfile/prototype/load')
def load_initfile_prototype(namefile: str, path: str, name: str, version: str,
                            current_user: UserModel = Depends(get_current_active_user)):
    # todo: check, path must not ../../
    pathExtractPrototypeInitfile = f'{PrototypeInitFilesDir}/{name}/{version}/'

    if path != '':
        pathFormat = f'/{path}/'
    else:
        pathFormat = ''

    pathForRead = f'{pathExtractPrototypeInitfile}{os.listdir(pathExtractPrototypeInitfile)[0]}{pathFormat}/{namefile}'

    with open(pathForRead) as f:
        return f.read()


@app.post('/initfile/prototype/update')
def update_initfile_prototype(fileUpdatePrototype: FileUpdatePrototype,
                              current_user: UserModel = Depends(get_current_active_user)):
    pathExtractPrototypeInitfile = f'{PrototypeInitFilesDir}/{fileUpdatePrototype.name}/{fileUpdatePrototype.version}'

    path_create_file = f'{pathExtractPrototypeInitfile}/{os.listdir(pathExtractPrototypeInitfile)[0]}/{fileUpdatePrototype.path}/{fileUpdatePrototype.filename}'

    if fileUpdatePrototype.operation == 'update':
        with open(path_create_file, 'w') as f:
            f.write(fileUpdatePrototype.data)
    elif fileUpdatePrototype.operation == 'delete':
        if Path(path_create_file).is_dir():
            os.rmdir(path_create_file)
        else:
            os.remove(path_create_file)
    elif fileUpdatePrototype.operation == 'create':
        if fileUpdatePrototype.type == 'file':
            with open(path_create_file, 'w') as f:
                f.write(fileUpdatePrototype.data)
        elif fileUpdatePrototype.type == 'directory':
            Path(path_create_file).mkdir()

    return {'Status': 'Ok'}

    return FileResponse(dir_to_zip_file(pathExtractPrototypeInitfile))


def dir_to_zip_file(dir):
    in_memory_output_file = io.BytesIO()
    zip_file_object = zipfile.ZipFile(in_memory_output_file, 'w')
    for root, dirs, files in os.walk(dir):
        for file in files:
            zip_file_object.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dir))

    zip_file_object.close()

    in_memory_output_file.seek(0)
    return in_memory_output_file


@app.get('/initfile/prototype/zip')
def get_zip_prototype(name: str, version: str):
    initfile = db_get_init_files(name, version)
    pathExtractPrototypeInitfile = f'{PrototypeInitFilesDir}/{name}/{version}'

    return StreamingResponse(dir_to_zip_file(pathExtractPrototypeInitfile), media_type="application/x-zip-compressed", )


@app.get('/api/text')
def add_task(context: str, text: str):
    import requests
    return json.loads(requests.get(config.server_ai + f'?context={context}&text={text}').text)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
