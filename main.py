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
    uvicorn.run(app, host="localhost", port=5000, log_level="info")