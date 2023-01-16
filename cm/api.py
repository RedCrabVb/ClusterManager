import paramiko
from ping3 import ping
from fastapi import FastAPI, Body
from fastapi import File, UploadFile
from cm.db import *
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.post("/upload")
def upload(file: UploadFile = File(...)):#name cluster
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:#unzip
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


class Item(BaseModel):
    name: str
    namefile: str
    data: str



@app.get('/tasks')
def list_tasks():
    return []


@app.get('/host')
def list_host():
    return db['hosts']


@app.post('/host')
def add_host(hostname: str, username: str, password: str):
    db['hosts'].append({hostname, username, password})
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


@app.get('/initfile')
def list_init_file():
    return db.get('init_files')


@app.post("/upload/initfile/test")
def upload(item: Item):#name cluster
    print(item)
    add_init_file('name', item.name)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

