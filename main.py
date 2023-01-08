import uvicorn

from cm import api
from cm.model import *

if __name__ == '__main__':
    print('Start ClusterManager')

    # # TODO: download hadoop
    # # TODO: format vars
    # # user: load config
    # serviceInit = ServiceTemplate('INIT_HADOOP', 'Init service hadoop',
    #                               [Action('etc_hosts_update', 'Add info about hosts to /etc/hosts',
    #                                       'ansible-playbook -i hosts/host network.yml'),
    #                                Action('copy_file_hadoop', 'Copy hadoop from local FS',
    #                                       'scp {download_path_with_file} {username_master}@{hostname_master}:{download_path}'),
    #                                Action('download_from_server', 'Download hadoop from URL',
    #                                       'wget {remote_server_uri} -d {download_path}')
    #                                ], None, [
    #                                   Vars('action', None, 'copy_file_hadoop',
    #                                        ['download_path_with_file', 'username_master', 'hostname_master',
    #                                         'download_path']),
    #                                   Vars('action', None, 'download_from_server',
    #                                        ['remote_server_uri', 'download_path'])
    #                               ])
    # # serviceInit
    #
    # # user: load config
    # serviceHdfs = ServiceTemplate('HDFS_INSTALL', 'Install hdfs', [
    #     Action('install_master', 'Install master', 'ansible-playbook -i hosts/host master.yml'),
    #     Action('install_worker', 'Install worker', 'ansible-playbook -i hosts/host workers.yml'),
    #     Action('add_host_TODO', 'Add hosts', 'config hosts change; install worker')
    # ], [ServiceRequirementGroup('master', 1, 1), ServiceRequirementGroup('workers', 1, None)], None)
    # # serviceHive = ServiceTemplate('Hive')
    # # servicePostgres = ServiceTemplate('Postgres')
    # installationFile = [serviceInit.to_json(), serviceHdfs.to_json()]
    # print(json.dumps(installationFile))

    with open('ConfigHadoop/hadoop-ansible/conf.json') as f:
        data = json.loads(f.read())
        init_file = [ServiceTemplate(**s) for s in data]

    for i_file in init_file:
        if i_file.extid == 'INIT_HADOOP':
            serviceInit = i_file
        if i_file.extid == 'HDFS_INSTALL':
            serviceHdfs = i_file

    # user: add host
    hostMaster = Host('192.168.56.121', 'root', '1234')
    hostWorker = Host('192.168.56.119', 'root', '1234')
    print(hostMaster.test_connection())
    # print(hostWorker.test_connection())

    # user: host move to cluster.
    # cluster example???
    # {"InitService": {"action_vars": {"copy_file_hadoop": {"download_path": null, "download_path_with_file": null, "hostname_master": null, "username_master": null}, "download_from_server": {"path_home": null, "uri": null}}, "actions": [{"extid": "etc_hosts_update", "name": "Add info about hosts to /etc/hosts", "params": null, "shell": "ansible-playbook -i hosts/host network.yml"}, {"extid": "copy_file_hadoop", "name": "Copy hadoop from local FS", "params": null, "shell": "scp {file} {username}@{hostname}:{path_home}"}, {"extid": "download_from_server", "name": "Download hadoop from URL", "params": null, "shell": "wget {uri} -d {path_home}"}], "extid": "INIT_HADOOP", "files_vars": {}, "hosts": [], "name": "Init service hadoop", "requirements_groups": null, "vars": [{"description": ["download_path_with_file", "username_master", "hostname_master", "download_path"], "extid": "copy_file_hadoop", "file": null, "type": "action"}, {"description": ["uri", "path_home"], "extid": "download_from_server", "file": null, "type": "action"}]}, "HdfsService": {"action_vars": {}, "actions": [{"extid": "install_master", "name": "Install master", "params": null, "shell": "ansible-playbook -i hosts/host master.yml"}, {"extid": "install_worker", "name": "Install worker", "params": null, "shell": "ansible-playbook -i hosts/host workers.yml"}, {"extid": "add_host_TODO", "name": "Add hosts", "params": null, "shell": "config hosts change; install worker"}], "extid": "HDFS_INSTALL", "files_vars": {}, "hosts": [{"group": "master", "hostname": "192.168.56.118", "password": "1234", "username": "root"}, {"group": "workers", "hostname": "192.168.56.119", "password": "1234", "username": "root"}], "name": "Install hdfs", "requirements_groups": [{"count": 1, "quantity_max": 1, "type_host": "master"}, {"count": 1, "quantity_max": null, "type_host": "workers"}], "vars": null}, "ActionTODO": ["stop", "run", "addHost"]}
    serviceHdfs.add_host(hostMaster, 'master')
    serviceHdfs.add_host(hostWorker, 'workers')
    # serviceHdfs.add_host(hostWorker2, 'workers')
    serviceHdfs.save_hosts_to_cluster('ConfigHadoop/hadoop-ansible')

    serviceInit.vars_apply()

    # 'scp {file} {username}@{hostname}:{path_home}'
    serviceInit.copy_file_hadoop = {}
    serviceInit.copy_file_hadoop['download_path_with_file'] = '/mnt/f/Download/tar/hadoop-3.2.4.tar.gz'
    serviceInit.copy_file_hadoop['username_master'] = hostMaster.username
    serviceInit.copy_file_hadoop['hostname_master'] = hostMaster.hostname
    serviceInit.copy_file_hadoop['download_path'] = f'/{hostMaster.username}'
    serviceInit.__setattr__('cluster_path', 'ConfigHadoop/hadoop-ansible')

    installationFile = [serviceInit.to_json(), serviceHdfs.to_json()]
    print(json.dumps(installationFile))
    # serviceInit.run_action_sh('etc_hosts_update', 'ConfigHadoop/hadoop-ansible')
    serviceInit.run_action_sh('copy_file_hadoop', serviceInit.cluster_path, serviceInit.copy_file_hadoop)
    # serviceHdfs.run_action_sh('install_master', 'ConfigHadoop/hadoop-ansible')
    # serviceHdfs.run_action_sh('install_worker', 'ConfigHadoop/hadoop-ansible')
    # TODO: format file dir hadoop ansible
    # TODO: run action from command

    uvicorn.run(api.app, host="localhost", port=5000, log_level="info")
