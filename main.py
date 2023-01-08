import json
import subprocess

import uvicorn

from cm import api
from cm.model import *

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

if __name__ == '__main__':
    print('Start ClusterManager')

    # TODO: download hadoop
    # TODO: format vars
    # TODO: service should describe requirements groups
    serviceInit = ServiceTemplate('INIT_HADOOP', 'Init service hadoop',
                                  [Action('etc_hosts_update', 'Add info about hosts to /etc/hosts', 'ansible-playbook -i hosts/host network.yml')], None)

    serviceHdfs = ServiceTemplate('HDFS_INSTALL', 'Install hdfs', [
        Action('install_master', 'Install master', 'Install master'),
        Action('install_worker', 'Install worker', 'Install worker'),
        Action('add_host', 'Add hosts', 'config hosts change; install worker')
    ], [ServiceRequirementGroup('master', 1, 1), ServiceRequirementGroup('workers', 1, None)])
    # serviceHive = ServiceTemplate('Hive')
    # servicePostgres = ServiceTemplate('Postgres')
    installationFile = {'InitService': serviceInit.to_json(), 'HdfsService': serviceHdfs.to_json(),
                        'ActionTODO': ['stop', 'run', 'addHost']}

    hostMaster = Host('192.168.56.118', 'root', '1234')
    hostWorker = Host('192.168.56.119', 'root', '1234')
    # hostWorker2 = Host('192.168.56.11944', 'root', '1234')
    print(hostMaster.test_connection())
    print(hostWorker.test_connection())
    # print(hostMaster.)

    print(json.dumps(installationFile))

    serviceHdfs.add_host(hostMaster, 'master')
    serviceHdfs.add_host(hostWorker, 'workers')
    # serviceHdfs.add_host(hostWorker2, 'workers')
    serviceHdfs.save_hosts_to_cluster('ConfigHadoop/hadoop-ansible')

    serviceInit.run_action_sh('etc_hosts_update', 'ConfigHadoop/hadoop-ansible')
    # TODO: format file dir hadoop ansible
    # TODO: run action from command

    uvicorn.run(api.app, host="localhost", port=5000, log_level="info")
