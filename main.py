import json
import subprocess

import paramiko
import uvicorn
from fastapi import FastAPI
from ping3 import ping

app = FastAPI()

hosts = [
    {
        'id': 1,
        'hostname': '192.168.56.114',
        'port': 21,
        'username': 'root',
        'password': '1234',
        'private_ssh': None
    },
    {
        'id': 2,
        'hostname': '192.138.56.114',
        'port': 21,
        'username': 'root3',
        'password': '1234',
        'private_ssh': None
    }
]


# host
# add to CM
# check/ping connection
#

# cluster = [
#     {
#         'id': 1,
#         'name': 'test cluster',
#         'description': 'description cluster',
#         'services': [],
#         'hosts': []
#     }
# ]

# service = {
#     'id': 1,
#     'name': 'name service',
#     'install_command_ansibele': "run install job",
#     'active': 'stop/start'
# }
# service.config.addParams
# service.config.addHost

# job = {
#     'id': 1,
#     'name': 'install hadoop',
#     'commands_ansible_script': ["check", "install", "test"]
# }
#

# add bundle

# list cluster

# job run:
# list host get
# gen on list host
# gen config
# run ansible script

class Cluster:
    def __int__(self, _id, _name, _description, _service, _hosts, _init_service):
        self.id = _id
        self.name = _name
        self.description = _description
        self.service = _service
        self.serviceInstall = _service
        self.init_service = _init_service
        self.hosts = _hosts


class Service:

    def __init__(self, _id, _name, _actions, _idCluster, _hosts):
        self.id = _id
        self.name = _name
        self.actions = _actions
        self.idCluster = _idCluster
        self.hosts = _hosts


class ServiceTemplate:

    def __init__(self, _extid, _name, _actions):
        self.extid = _extid
        self.name = _name
        self.actions = _actions

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))


class Action:

    def __init__(self, _extid, _name, _shell):
        self.extid = _extid
        self.name = _name
        self.shel = _shell


class Host:

    def __init__(self, _hostname, _username, _password):
        self.hostname = _hostname
        self.username = _username
        self.password = _password

    def test_connection(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.load_system_host_keys()
            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)
            ssh_client.close()
            return True
        except paramiko.ssh_exception.AuthenticationException as e:
            return False

    def run_shell(self, command):
        params_ssh = '-o StrictHostKeyChecking=no '
        shell_execute = f'sshpass -p "{self.password}" ssh {params_ssh} {self.username}@{self.hostname} {command}'
        print(shell_execute)
        return_code = subprocess.call(shell_execute, shell=True)

        return return_code


class HostInCluster:
    def __init__(self, _host, group, ):
        self.hostname = _host.hostname
        self.username = _host.username
        self.password = _host.password


@app.get('/hosts')
def get_hosts():
    return ({'hosts': hosts})


@app.route('/hosts', methods=['PUT'])
def put():
    hosts.append(None)


@app.get('/host')
def host_ping(id: int):
    host = None
    for i_host in hosts:
        if i_host['id'] == id:
            host = i_host

    print(id)
    # verbose_ping(host['hostname'], count=3)
    delay = ping(host['hostname'], timeout=2)
    return {'id': id, 'delay': delay}


@app.get('/host/shell')
def host_shell_execute(shell, id: int):
    print(shell)

    host = None
    for i_host in hosts:
        if i_host['id'] == id:
            host = i_host

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
    stdin, out, err = ssh_client.exec_command(shell)
    # out.read()
    return out.readline()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    print('Start ClusterManager')

    serviceInit = ServiceTemplate('INIT_HADOOP', 'Init service hadoop',
                                  [Action('etc_hosts_update', 'Add info about hosts to /etc/hosts', 'ansible ...')])
    serviceHdfs = ServiceTemplate('HDFS_INSTALL', 'Install hdfs', [
        Action('install_master', 'Install master', 'Install master'),
        Action('install_worker', 'Install worker', 'Install worker'),
        Action('add_host', 'Add hosts', 'config hosts change; install worker')
    ])
    # serviceHive = ServiceTemplate('Hive')
    # servicePostgres = ServiceTemplate('Postgres')
    installationFile = {'InitService': serviceInit.to_json(), 'HdfsService': serviceHdfs.to_json(),
                        'ActionTODO': ['stop', 'run', 'addHost']}

    hostMaster = Host('192.168.56.118', 'root', '1234')
    print(hostMaster.test_connection())

    hostMaster.run_shell('echo "baddddd" >> /root/bllb')

    print(json.dumps(installationFile))

    # uvicorn.run(app, host="localhost", port=5000, log_level="info")
