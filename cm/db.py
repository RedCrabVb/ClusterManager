# todo: connect to postgres, postgres continue table

db = {
    'hosts': [],
    'init_files': [
    {
        "version": "v0",
        "namefile": "hadoop-ansible.zip",
        "name": "hadoop"
    }
    ],
    'clusters': []
}


def add_init_file(name, namefile, version):
    # todo: path FS
    db.get('init_files').append({"name": name, "namefile": namefile, "version": version})


def create_cluster(cluster):
    # todo: cp i_file to new dir
    db['clusters'].append(cluster)

