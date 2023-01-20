from fastapi import FastAPI, Body
from cm.db import *
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from pathlib import Path

from cm.model import Host

InitFilesDir = './TmpConfigHadoop'

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


class TaskRunAction(BaseModel):
    # type: str # add_host cluster, test_connection, run_action,
    cluster: str
    extid_action: str


@app.post('/task/test_connection')
def test_connection(host: Host):
    # TODO: async
    print('test connection')

    print(host)
    return {'Status': host.test_connection()}

@app.post('/task/run_action')
def add_task(any):
    print(any)


@app.get('/tasks')
def list_tasks():
    return []


@app.get('/host')
def list_host():
    return db['hosts']


@app.post('/host')
def add_host(host: Host):
    for h in db['hosts']:
        if h['hostname'] == host.hostname and h['username'] == host.username:
            raise Exception('This host exists')

    db['hosts'].append({'hostname': host.hostname, 'username': host.username, 'password' : host.password, 'status_connect': False})
    return {'Status': 'Ok'}


@app.get('/cluster')
def list_cluster(name):
    # json ret
    # list var
    # list change
    return db['clusters']


@app.get('/cluster')
def list_cluster():
    return db['clusters']


@app.post('/cluster')
def create_cluster(name: str, description: str, initfile_name: str):
    item: Item = db.get(initfile_name)

    print('cp item.data')

    create_cluster({name, description, item})
    return {'Status': 'Ok'}


# dev
@app.get('/initfile')
def list_init_file():
    return db.get('init_files')


# dev
@app.post("/upload/initfile/test")
def upload(item: Item):  # name cluster

    print(item)

    Path(f'{InitFilesDir}/{item.name}').mkdir(parents=True, exist_ok=True)
    with open(f'{InitFilesDir}/{item.name}/{item.namefile}', 'wb') as finit:
        finit.write(base64.standard_b64decode(item.data))

    # todo: unzip

    add_init_file(item.name, item.namefile, 'v0')


@app.get("/")
async def read_root():
    return {"Hello": "World"}
