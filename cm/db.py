# todo: connect to postgres, postgres continue table

db = {
    'hosts': [],
    'init_files': [],
    'clusters': []
}


def add_init_file(i):
    # todo: path FS
    db['init_files'].append(i)


def create_cluster(i_file):
    # todo: cp i_file to new dir
    db['clusters'].append(None)

