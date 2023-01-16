# todo: connect to postgres, postgres continue table

db = {
    'hosts': [],
    'init_files': [],
    'clusters': []
}


def add_init_file(name, version):
    # todo: path FS
    db.get('init_files').append({name, version})


def create_cluster(cluster):
    # todo: cp i_file to new dir
    db['clusters'].append(cluster)

