from flask import Flask, jsonify, request
import paramiko
from ping3 import ping, verbose_ping

app = Flask(__name__)

hosts = [
    {
        'id': 1,
        'hostname': '192.168.56.110',
        'port': 21,
        'username': 'root',
        'password': '1234',
        'private_ssh': None
    },
    {
        'id': 2,
        'hostname': '192.138.56.110',
        'port': 21,
        'username': 'root3',
        'password': '1234',
        'private_ssh': None
    }
]


@app.route('/hosts', methods=['GET'])
def get_hosts():
    return jsonify({'hosts': hosts})


@app.route('/hosts', methods=['PUT'])
def put():
    hosts.append(None)


@app.route('/host', methods=['GET'])
def host_ping():
    id = request.args.get('id', default=1, type=int)

    host = None
    for i_host in hosts:
        if i_host['id'] == id:
            host = i_host

    print(id)
    # verbose_ping(host['hostname'], count=3)
    delay = ping(host['hostname'], timeout=2)
    return {'id': id, 'delay': delay}


@app.route('/host/shell', methods=['GET'])
def host_shell_execute():
    shell = request.args.get('shell')
    id = request.args.get('id', type=int)
    print(shell)

    host = None
    for i_host in hosts:
        if i_host['id'] == id:
            host = i_host

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(hostname=host['hostname'], username=host['username'], password=host['password'])
    stdin, out, err = ssh_client.exec_command(shell)
    out.read()
    return out.readline()


if __name__ == '__main__':
    print('Start ClusterManager')
    app.run(debug=True)
