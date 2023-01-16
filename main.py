import uvicorn

# from cm import api
from cm.model import *

import cm.api

if __name__ == '__main__':
    print('Start ClusterManager')
    uvicorn.run(cm.api.app, host="localhost", port=5000, log_level="info")

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

    print('load config')
    with open('ConfigHadoop/hadoop-ansible/conf.json') as f:
        data = json.loads(f.read())
        init_file = [ServiceTemplate(**s) for s in data]

    for i_file in init_file:
        if i_file.extid == 'INIT_HADOOP':
            serviceInit = i_file
        if i_file.extid == 'HDFS_INSTALL':
            serviceHdfs = i_file

    print('user: add host')
    hostMaster = Host('192.168.56.125', 'root', '1234')
    hostWorker = Host('192.168.56.126', 'root', '1234')
    hostWorker2 = Host('192.168.56.127', 'root', '1234')
    print(hostMaster.test_connection())
    print(hostWorker.test_connection())
    print(hostWorker2.test_connection())
    # print(hostWorker.test_connection())

    # user: host move to cluster.
    # cluster example???
    serviceInit.__setattr__('cluster_path', 'ConfigHadoop/hadoop-ansible')

    print('host move to cluster.')
    serviceHdfs.install_worker = {'master_ip': hostMaster.hostname, 'master_hostname': hostMaster.hostname}
    serviceHdfs.add_host(hostMaster, 'master')
    serviceHdfs.add_host(hostWorker, 'workers')
    serviceHdfs.add_host(hostWorker2, 'workers')
    # serviceHdfs.add_host(hostWorker2, 'workers')
    serviceHdfs.save_hosts_to_cluster(serviceInit.cluster_path)

    # serviceInit.vars_apply()

    # 'scp {file} {username}@{hostname}:{path_home}'
    serviceInit.copy_file_hadoop = {'download_path_with_file': '/mnt/f/Download/tar/hadoop-3.2.4.tar.gz',
                                    'username_master': hostMaster.username, 'password_master': hostMaster.password, 'hostname_master': hostMaster.hostname,
                                    'download_path': '/' + hostMaster.username}



    # installationFile = [serviceInit.to_json(), serviceHdfs.to_json()]
    # print(json.dumps(installationFile))
    serviceInit.run_action_sh('etc_hosts_update', 'ConfigHadoop/hadoop-ansible')
    serviceInit.run_action_sh('copy_file_hadoop', serviceInit.cluster_path, serviceInit.copy_file_hadoop)
    # TODO: how to update vars .yaml?
    serviceHdfs.run_action_sh('install_master', 'ConfigHadoop/hadoop-ansible')
    serviceHdfs.run_action_sh('install_worker', 'ConfigHadoop/hadoop-ansible', serviceHdfs.install_worker)

