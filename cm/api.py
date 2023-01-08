import paramiko
from ping3 import ping
from fastapi import FastAPI

app = FastAPI()

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
