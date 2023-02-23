import json
import os
import socket
import subprocess
from threading import Thread

import paramiko
from itertools import groupby
import logging

import psycopg2
from pydantic import BaseModel

from cm.db import conn

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


wd = os.getcwd()
encodings_console = os.environ['ENCODING_CONSOLE']


class RunProcess:
    def __init__(self):
        self.return_code = None

    def do(self, shell_command):
        p = subprocess.Popen(shell_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            return_code = p.poll()
            line = p.stdout.readline()
            line_decode = line.decode(encodings_console)
            yield line_decode
            if return_code is not None:
                self.return_code = return_code
                break


def init_proc(execute_shell: str, extid_action: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        cursor.execute('INSERT INTO process(command, extid_action, date_start) values (%s, %s, now())  returning id',
                       (execute_shell, extid_action))
        proc_id = cursor.fetchone()[0]
        return proc_id


def log_proc_db(proc_id: int, execute_shell: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

        proc = RunProcess()
        for line_output in proc.do(execute_shell):
            cursor.execute('UPDATE process SET stdout = stdout || %s WHERE id = %s', (line_output, proc_id,))
        cursor.execute('UPDATE process SET is_complite = true, code_return = %s '
                       'WHERE id = %s',
                       (proc.return_code, proc_id,))


class ServiceTemplate:

    def __init__(self, my_dict):

        for key in my_dict:
            setattr(self, key, my_dict[key])

    def add_host(self, host, group):
        add_host = False

        for r in self.requirements_groups:
            if r['type_host'] == group:
                cont_group_in_cluster = 0
                for h in self.hosts:
                    print(group)
                    print(h)
                    if h['group'] == group:
                        cont_group_in_cluster += 1

                if r['quantity_max'] is None:
                    add_host = True
                else:
                    add_host = cont_group_in_cluster < r['quantity_max']

        if not add_host:
            raise Exception('The host does not meet the cluster requirements, either the wrong cluster group is '
                            'specified, or enough hosts have already been installed')

        self.hosts.append({'hostname': host.hostname, 'username': host.username,
                           'password': host.password, 'group': group})

    # Remove from this class
    # passable, move to ansible?
    def save_hosts_to_cluster(self, path_cluster):
        subprocess.run(f'export ANSIBLE_CONFIG={os.getcwd()}/{path_cluster}', shell=True)
        with open(path_cluster + "/vars/var_list_host.yml", 'w') as f:
            f.write('iter:\n')
            for i, h in enumerate(self.hosts):
                f.write(f'''  - key: {h['group']}{i}
    val: {h['hostname']}\n''')

        sorted_hosts = sorted(self.hosts, key=lambda host: host['group'])
        grouped = [list(result) for key, result in groupby(
            sorted_hosts, key=lambda host: host['group'])]

        with open(path_cluster + "/hosts/host", 'w') as f:
            for g in grouped:
                f.write('[{}]\n'.format((g[0]['group'])))
                for g2 in g:
                    f.write(g2['hostname'] + f' ansible_user={g2["username"]} ansible_ssh_pass={g2["password"]}\n')

    # todo: must move to run job service
    # Remove from this class
    def run_action_sh(self, extid_action, path_cluster, vars_shell=None):
        os.chdir(wd)
        os.chdir(path_cluster)
        for a in self.actions:
            if a['extid'] == extid_action:
                execute_shell = a['shell']
                if vars_shell is not None:
                    execute_shell = execute_shell.format(**vars_shell)

                logging.info(f'Execute action extid: {extid_action}, shell: {execute_shell}')

                proc_id = init_proc(execute_shell, extid_action)
                Thread(target=log_proc_db, args=(proc_id, execute_shell)).start()

                os.chdir(wd)
                return proc_id

        os.chdir(wd)
        raise Exception(f'Not found action with extid {extid_action}')

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))


class HostService(BaseModel):
    hostname: str
    username: str
    password: str

    # Remove from this class?
    def test_connection(self):
        try:
            ssh_client = paramiko.SSHClient()

            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)
            ssh_client.close()
            return True
        except paramiko.ssh_exception.AuthenticationException:
            return False
        except socket.gaierror as er:
            return False

    # Remove from this class?
    def run_shell(self, command):
        params_ssh = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no '
        shell_execute = f'sshpass -p "{self.password}" ssh {params_ssh} {self.username}@{self.hostname} {command}'
        print(shell_execute)
        return_code = subprocess.call(shell_execute, shell=True)

        return return_code
