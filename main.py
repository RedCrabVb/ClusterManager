from flask import Flask, jsonify, request

app = Flask(__name__)

hosts = [
    {
        'id': 1,
        'name': 'host1',
        'user': 'admin',
        'password': 'password',
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
    id = request.args.get('id', default = 1, type = int)
    print(id)
    return {'id': id}

@app.route('/hosts', methods=['GET'])
def host_shell_execute():
    shell = request.args.get('shell')
    print(shell)
    return shell

if __name__ == '__main__':
    print('Start ClusterManager')
    app.run(debug=True)
