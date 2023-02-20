import json
import os
import sqlite3

import psycopg2.extras
from fastapi import FastAPI
from psycopg2 import sql

from cm.db import *
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from pathlib import Path

from cm.model import Host, ServiceTemplate

InitFilesDir = './TmpConfigHadoop'
ClusterDir = './TmpConfigHadoop/Cluster'

origins = [
    "http://localhost:4200",
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

app = FastAPI(middleware=middleware)


class ItemInitFile(BaseModel):
    name: str
    namefile: str
    data: str


class ItemAddClusterHost(BaseModel):
    name_cluster: str
    host: Host
    group: str
    extid_service: str


class TaskRunAction(BaseModel):
    # type: str # add_host cluster, test_connection, run_action,
    cluster: str
    extid_action: str
    intifle_name: str


class ClusterUser(BaseModel):
    name: str
    description: str
    initfile_name: str


class UpdateConfigItem(BaseModel):
    cluster_name: str
    config_name: str
    config_file: str


class RunActionModel(BaseModel):
    cluster_name: str
    extid: str
    extid_service: str
    shell_parameters: dict


@app.post('/task/test_connection')
def test_connection(host: Host):
    # TODO: async
    print('test connection')

    print(host)
    return {'Status': host.test_connection()}


@app.post('/task/run_action')
def add_task(runActionModel: RunActionModel):
    print('asdf')
    for c in db['clusters']:
        if c['name'] == runActionModel.cluster_name:
            print(c['name'])
            for i_file in c['data']:
                if i_file['extid'] == runActionModel.extid_service:
                    service_tmp = ServiceTemplate(i_file)
                    service_tmp.run_action_sh(runActionModel.extid, c['pathClusterDir'], runActionModel.shell_parameters)


@app.get('/task/get_json_cluster')
def add_task(name_cluster: str):
    for c in db['clusters']:
        if c['name'] == name_cluster:
            return c
    raise Exception('Not found cluster')


@app.get('/tasks')  # todo
def list_tasks():
    return []


@app.get('/hosts')
def list_host():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM hosts')
        records = cursor.fetchall()
        for ix in records:
            print(dict(ix))

        return [dict(ix) for ix in records]


@app.post('/host/delete')
def delete_host(host: Host):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM hosts WHERE hostname = %s and username = %s', (host.hostname, host.username))

    return {'Status': 'Ok'}


@app.post('/host')
def add_host(host: Host):
    with conn.cursor() as cursor:
        conn.autocommit = True
        insert_host = sql.SQL('insert into hosts (hostname, username, password, status_connect) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(host.hostname, host.username, host.password, False)]))
        )
        cursor.execute(insert_host)

    return {'Status': 'Ok'}


@app.get('/cluster')
def list_cluster():
    return db['clusters']


@app.post('/cluster/host/save')
def save_host(name_cluster: str, extid_service: str):
    for c in db['clusters']:
        if c['name'] == name_cluster:
            for s in c['data']:
                if s['extid'] == extid_service:
                    service = ServiceTemplate(s)
                    service.save_hosts_to_cluster(c['pathClusterDir'])


@app.post("/cluster/host")
def add_host_to_cluster(itemAddClusterHost: ItemAddClusterHost):
    for c in db['clusters']:
        if c['name'] == itemAddClusterHost.name_cluster:
            for s in c['data']:
                if s['extid'] == itemAddClusterHost.extid_service:
                    service = ServiceTemplate(s)
                    service.add_host(itemAddClusterHost.host, itemAddClusterHost.group)


@app.get('/cluster/conf/list')
def get_conf_list(cluster_name: str):
    for c in db['clusters']:
        if c['name'] == cluster_name:
            configs = []
            for (path, dirnames, filenames) in os.walk(c['pathClusterDir'] + '/vars'):
                for f in filenames:
                    with open(c['pathClusterDir'] + '/vars/' + f) as fcontent:
                        configs.append({'filename': f, 'content': fcontent.read()})

            return configs
    raise Exception('Not found conf')


@app.post('/cluster/conf/update')
def update_conf(cluster: UpdateConfigItem):
    for c in db['clusters']:
        if c['name'] == cluster.cluster_name:
            path_conf = c['pathClusterDir']
            with open(f'{path_conf}/vars/{cluster.config_name}', 'w') as finit:
                finit.write(cluster.config_file)
                return {'Status', 'Ok'}

    raise Exception('Not found conf')


@app.post('/cluster')
def create_cluster(cluster: ClusterUser):
    import zipfile
    import os

    (name_initfile, version_cluster) = cluster.initfile_name.split('|')
    for ifile in db['init_files']:
        if ifile['version'] == version_cluster and ifile['name'] == name_initfile:
            item = ifile

    item_name = item['name']
    item_namefile = item['namefile']
    item_version = item['version']
    path_initfile = Path(f'{InitFilesDir}/{item_name}/{item_namefile}')
    path_cluster_dir = Path(f'{ClusterDir}/{cluster.name}/{item_name}/{item_version}')
    path_cluster_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(path_initfile, 'r') as zip_ref:
        zip_ref.extractall(path_cluster_dir)

    cluster_files = f'{path_cluster_dir}/{next(os.walk(path_cluster_dir))[1][0]}'

    with open(f'{cluster_files}/conf.json') as f:
        data = json.loads(f.read())
        print(data)

    print('cp item.data')

    db['clusters'].append({"name": cluster.name, "description": cluster.description, "item": item, "data": data,
                           "pathClusterDir": f'{cluster_files}'})
    return {'Status': 'Ok'}


# dev
@app.get('/initfile')
def list_init_file():
    return db.get('init_files')


@app.post("/upload/initfile")
def upload(item: ItemInitFile):
    Path(f'{InitFilesDir}/{item.name}').mkdir(parents=True, exist_ok=True)
    with open(f'{InitFilesDir}/{item.name}/{item.namefile}', 'wb') as finit:
        finit.write(base64.standard_b64decode(item.data))

    # todo: unzip

    add_init_file(item.name, item.namefile, 'v0')


@app.get("/")
async def read_root():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hosts')
    records = cursor.fetchall()
    print(''.join(records))
    cursor.close()
    conn.close()

    return {"Hello": "World"}
