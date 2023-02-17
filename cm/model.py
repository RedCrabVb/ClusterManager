import json
import os
import socket
import subprocess

import paramiko
from itertools import groupby

from pydantic import BaseModel


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

    def __init__(self, my_dict):

        for key in my_dict:
            setattr(self, key, my_dict[key])

    # def __init__(self, extid, name, actions,
    #              requirements_groups,
    #              vars_service,
    #              action_vars=None, files_vars=None, hosts=None):
    #     self.extid = extid
    #     self.name = name
    #     self.actions = actions
    #     self.requirements_groups = requirements_groups
    #     self.vars_service = vars_service
    #     self.action_vars = {}
    #     self.files_vars = {}
    #     self.hosts = []

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
        return_code = subprocess.run(f'export ANSIBLE_CONFIG={os.getcwd()}/{path_cluster}', shell=True)
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
                    f.write(g2.hostname + f' ansible_user={g2.username} ansible_ssh_pass={g2.password}\n')

    # todo: must move to run job service
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

        os.chdir(wd)
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


class Host(BaseModel):
    hostname: str
    username: str
    password: str

    def test_connection(self):
        try:
            ssh_client = paramiko.SSHClient()

            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)
            ssh_client.close()
            return True
        except paramiko.ssh_exception.AuthenticationException as e:
            return False
        except socket.gaierror as er:
            return False

    def run_shell(self, command):
        params_ssh = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no '
        shell_execute = f'sshpass -p "{self.password}" ssh {params_ssh} {self.username}@{self.hostname} {command}'
        print(shell_execute)
        return_code = subprocess.call(shell_execute, shell=True)

        return return_code
