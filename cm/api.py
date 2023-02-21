import fnmatch
import json
import os
import zipfile

import psycopg2.extras
from fastapi import FastAPI
from psycopg2 import sql

from cm.db import *
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
import base64
import shutil
from pathlib import Path

from cm.model import ServiceTemplate

from cm.base_model import *

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


@app.post('/task/test_connection')
def test_connection(host: Host):
    # TODO: async
    print('test connection')

    print(host)
    return {'Status': host.test_connection()}


@app.post('/task/run_action')
def add_task(runActionModel: RunActionModel):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (runActionModel.cluster_name,))
        records = cursor.fetchone()
        # print(records['name'])
        for i_file in json.loads(records['data']):
            if i_file['extid'] == runActionModel.extid_service:
                service_tmp = ServiceTemplate(i_file)
                service_tmp.run_action_sh(runActionModel.extid, records['path_cluster_dir'],
                                          runActionModel.shell_parameters)


@app.get('/hosts')
def list_host():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM hosts')
        records = cursor.fetchall()

        return [dict(ix) for ix in records]


@app.post('/host/delete')
def delete_host(host: Host):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM hosts WHERE hostname = %s and username = %s', (host.hostname, host.username))

    return {'Status': 'Ok'}


@app.post('/host')
def add_host(host: Host):
    with conn.cursor() as cursor:
        insert_host = sql.SQL('insert into hosts (hostname, username, password, status_connect) values {}').format(
            sql.SQL(',').join(map(sql.Literal, [(host.hostname, host.username, host.password, False)]))
        )
        cursor.execute(insert_host)

    return {'Status': 'Ok'}


@app.get('/cluster')
def list_cluster():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters')
        records = cursor.fetchall()

        results = [dict(ix) for ix in records]
        for result in results:
            result['data'] = json.loads(result['data'])
            result['item'] = json.loads(result['item'])

    return results


@app.post('/cluster/host/save')
def save_host(name_cluster: str, extid_service: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (name_cluster,))
        records = cursor.fetchone()

        for s in json.loads(records['data']):
            if s['extid'] == extid_service:
                service = ServiceTemplate(s)
                service.save_hosts_to_cluster(records['path_cluster_dir'])


@app.post("/cluster/host")
def add_host_to_cluster(itemAddClusterHost: ItemAddClusterHost):
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
def get_conf_list(cluster_name: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('SELECT * FROM clusters WHERE name = %s', (cluster_name,))
        records = cursor.fetchone()

        configs = []
        for (path, dir_names, filenames) in os.walk(records['path_cluster_dir'] + '/vars'):
            for f in filenames:
                with open(records['path_cluster_dir'] + '/vars/' + f) as f_content:
                    configs.append({'filename': f, 'content': f_content.read()})

        return configs

    raise Exception('Not found conf')


@app.post('/cluster/delete')
def delete_cluster(clusterName: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters WHERE name = %s', (clusterName,))
        records = cursor.fetchone()

        shutil.rmtree(Path(records['path_cluster_dir']))

        cursor.execute('DELETE FROM clusters WHERE name = %s', (clusterName, ))

    return {'Status': 'Ok'}


@app.post('/cluster/conf/update')
def update_conf(cluster: ClusterUpdate):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM clusters WHERE name = %s', (cluster.cluster_name,))
        records = cursor.fetchone()

        path_conf = records['path_cluster_dir']
        with open(f'{path_conf}/vars/{cluster.config_name}', 'w') as f_init:
            f_init.write(cluster.config_file)
            return {'Status', 'Ok'}

    raise Exception('Not found conf')


@app.post('/cluster')
def create_cluster(cluster: ClusterUser):
    import zipfile
    import os

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
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
def delete_initfile(item_init_file: ItemInitFileVersion):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM init_files WHERE name = %s and version = %s',
                       (item_init_file.name, item_init_file.version))
        record_init_file = cursor.fetchone()

        shutil.rmtree(Path(f'{InitFilesDir}/{record_init_file["name"]}'))

        cursor.execute('DELETE FROM init_files WHERE name = %s and version = %s',
                       (item_init_file.name, item_init_file.version))

    return {'Status': 'Ok'}


@app.get('/initfile')
def list_init_file():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM init_files')
        records = cursor.fetchall()
        for ix in records:
            print(dict(ix))

        return [dict(ix) for ix in records]


@app.post("/upload/initfile")
def upload(item: ItemInitFile):
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
