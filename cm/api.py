import json

from fastapi import FastAPI, Body
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


# return cluster
# return host
# return cluster example
# change params cluster example action
# run action
# create cluster from template


class Item(BaseModel):
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


@app.post('/task/test_connection')
def test_connection(host: Host):
    # TODO: async
    print('test connection')

    print(host)
    return {'Status': host.test_connection()}


@app.post('/task/run_action')  # todo
def add_task(any):
    print(any)


@app.get('/tasks')  # todo
def list_tasks():
    return []


@app.get('/hosts')
def list_host():
    return db['hosts']


@app.post('/host/delete')
def delete_host(host: Host):
    new_db_hosts = []
    for h in db['hosts']:
        if not h['hostname'] == host.hostname or not h['username'] == host.username:
            new_db_hosts.append(h)

    db['hosts'] = new_db_hosts
    return {'Status': 'Ok'}


@app.post('/host')
def add_host(host: Host):
    for h in db['hosts']:
        if h['hostname'] == host.hostname and h['username'] == host.username:
            raise Exception('This host exists')

    db['hosts'].append(
        {'hostname': host.hostname, 'username': host.username, 'password': host.password, 'status_connect': False})
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
        # init_file = [ServiceTemplate(**s) for s in data]
        print(data)

    # +json load
    # ------json add variable
    # +json add path

    # user see to action
    # user change _dir file_
    # user change _vars file_
    # user add host and role

    # загружать файлы на сервер
    print('cp item.data')

    db['clusters'].append({"name": cluster.name, "description": cluster.description, "item": item, "data": data, "pathClusterDir": f'{cluster_files}'})
    return {'Status': 'Ok'}


# dev
@app.get('/initfile')
def list_init_file():
    return db.get('init_files')


@app.post("/upload/initfile")
def upload(item: Item):
    Path(f'{InitFilesDir}/{item.name}').mkdir(parents=True, exist_ok=True)
    with open(f'{InitFilesDir}/{item.name}/{item.namefile}', 'wb') as finit:
        finit.write(base64.standard_b64decode(item.data))

    # todo: unzip

    add_init_file(item.name, item.namefile, 'v0')


@app.get("/")
async def read_root():
    return {"Hello": "World"}
