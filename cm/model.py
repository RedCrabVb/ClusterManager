import json
import os
import subprocess

import paramiko
from itertools import groupby


# installationFile = {'InitService': serviceInit.to_json(), 'HdfsService': serviceHdfs.to_json(),
#                     'ActionTODO': ['stop', 'run', 'addHost']}
# class InitFile:
#     def __init__(self, _init_service):
#         self.init_service = _init_service
#         self.

class ServiceRequirementGroup:

    def __init__(self, type_host, count, quantity_max):
        self.type_host = type_host
        self.count = count
        self.quantity_max = quantity_max


class Cluster:
    def __int__(self, _id, _name, _description, _service, _hosts, _init_service):
        self.id = _id
        self.name = _name
        self.description = _description
        self.service = _service
        self.serviceInstall = _service
        self.init_service = _init_service
        self.hosts = _hosts


class Action:

    def __init__(self, extid, name, shell, params=None):
        self.extid = extid
        self.name = name
        self.shell = shell
        self.params = params

# class Service:
#
#     def __init__(self, _id, _name, _actions, _idCluster, _hosts):
#         self.id = _id
#         self.name = _name
#         self.actions = _actions
#         self.idCluster = _idCluster
#         self.hosts = _hosts

class Vars:

    def __init__(self, _type, _file, _extid, _description):
        self.type = _type
        self.file = _file
        self.extid = _extid
        self.description = _description

    def execute(self):
        if self.type == 'fileconf':
            import yaml

            yaml.load(self.file)
            # upd file
        elif self.type == 'action':
            print('action')


class ServiceTemplate:

    def __init__(self, extid, name, actions,
                 requirements_groups,
                 vars_service,
                 action_vars=None, files_vars=None, hosts=None):
        self.extid = extid
        self.name = name
        self.actions = actions
        self.requirements_groups = requirements_groups
        self.vars_service = vars_service
        self.action_vars = {}
        self.files_vars = {}
        self.hosts = []

    def vars_apply(self):
        for var in self.vars_service:
            if var['type'] == 'action':
                self.action_vars[var['extid']] = {}
                for attr in var['description']:
                    self.action_vars[var['extid']][attr] = None
            if var['type'] == 'file':
                pass

    def add_host(self, host, group):
        add_host = False

        for r in self.requirements_groups:
            if r['type_host'] == group:
                cont_group_in_cluster = 0
                for h in self.hosts:
                    print(group)
                    print(h)
                    if h.group == group:
                        cont_group_in_cluster += 1

                if not r['quantity_max'] is None:
                    add_host = cont_group_in_cluster < r['quantity_max']
                else:
                    add_host = True

        if not add_host:
            raise Exception('The host does not meet the cluster requirements, either the wrong cluster group is '
                            'specified, or enough hosts have already been installed')

        self.hosts.append(HostInCluster(host, group))

    def save_hosts_to_cluster(self, path_cluster):
        with open(path_cluster + "/vars/var_list_host.yml", 'w') as f:
            f.write('iter:\n')
            for i, h in enumerate(self.hosts):
                f.write(f'''  - key: {h.group}{i}
    val: {h.hostname}\n''')

        sorted_hosts = sorted(self.hosts, key=lambda h: h.group)
        grouped = [list(result) for key, result in groupby(
            sorted_hosts, key=lambda h: h.group)]

        with open(path_cluster + "/hosts/host", 'w') as f:
            for g in grouped:
                f.write(f'[{g[0].group}]\n')
                for g2 in g:
                    f.write(g2.hostname + '\n')

    def run_action_sh(self, extid_action, path_cluster, vars_shell=None):
        wd = os.getcwd()
        os.chdir(path_cluster)
        for a in self.actions:
            if a['extid'] == extid_action:
                execute_shell = a['shell']
                if vars_shell is not None:
                    execute_shell = execute_shell.format(**vars_shell)

                print(execute_shell)
                return_code = subprocess.call(execute_shell, shell=True)
                os.chdir(wd)
                return return_code

        raise Exception(f'Not found action with extid {extid_action}')

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))


class HostInCluster:
    def __init__(self, _host, _group):
        self.hostname = _host.hostname
        self.username = _host.username
        self.password = _host.password
        self.group = _group





class Host:

    def __init__(self, _hostname, _username, _password):
        self.hostname = _hostname
        self.username = _username
        self.password = _password

    def test_connection(self):
        try:
            subprocess.call(f'sshpass -p "{self.password}" ssh-copy-id {self.username}@{self.hostname}', shell=True)

            ssh_client = paramiko.SSHClient()
            ssh_client.load_system_host_keys()

            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password,
                               look_for_keys=False, allow_agent=False)
            ssh_client.close()
            return True
        except paramiko.ssh_exception.AuthenticationException as e:
            return False

    def run_shell(self, command):
        params_ssh = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no '
        shell_execute = f'sshpass -p "{self.password}" ssh {params_ssh} {self.username}@{self.hostname} {command}'
        print(shell_execute)
        return_code = subprocess.call(shell_execute, shell=True)

        return return_code
