import json
import logging
import os
import subprocess
from datetime import timedelta, datetime
from itertools import groupby
from threading import Thread

import paramiko
import psycopg2.extras
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from main_app import config
from main_app.cm.base_model import *
from main_app.cm.db import *
from main_app.config import ENCODING_CONSOLE

logging.basicConfig(filename=config.record_filename_log, level=config.level_log,
                    format=config.formate_log)

wd = os.getcwd()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class RunProcess:
    def __init__(self):
        self.return_code = None

    def do(self, shell_command, cwd):
        p = subprocess.Popen(shell_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=True)
        while True:
            return_code = p.poll()
            line = p.stdout.readline()
            line_decode = line.decode(ENCODING_CONSOLE)
            yield line_decode
            if return_code is not None:
                self.return_code = return_code
                break


def write_proc_to_db(execute_shell: str, extid_action: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO process(command, extid_action, date_start) values (%s, %s, now())  returning id',
                       (execute_shell, extid_action))
        proc_id = cursor.fetchone()[0]
        return proc_id


def log_proc_db(proc_id: int, execute_shell: str, cwd: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        proc = RunProcess()
        for line_output in proc.do(execute_shell, cwd):
            cursor.execute('UPDATE process SET stdout = stdout || %s WHERE id = %s', (line_output, proc_id,))
        cursor.execute('UPDATE process SET is_complite = true, code_return = %s '
                       'WHERE id = %s',
                       (proc.return_code, proc_id,))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM user_cm WHERE username = %s', (username,))
        records = cursor.fetchone()

        return UserModelInDB(username=records['username'], hashed_password=records['hash_password'])


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=config.expire_token)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataModel(username=username)
    except Exception:
        raise credentials_exception
    user = get_user(conn, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
                    logging.info(f'add host {h} {group}')

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

    # passable, move to ansible?
    def save_hosts_to_cluster(self, path_cluster):
        os.chdir(wd)

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
        os.putenv('ANSIBLE_CONFIG', os.getcwd())

        logging.info(f'Current dir {wd}, change dir {path_cluster}')
        for a in self.actions:
            if a['extid'] == extid_action:
                execute_shell = a['shell']
                if vars_shell is not None:
                    execute_shell = execute_shell.format(**vars_shell)

                logging.info(f'Execute action extid: {extid_action}, shell: {execute_shell}, In dir {os.listdir()}')

                proc_id = write_proc_to_db(execute_shell, extid_action)
                Thread(target=log_proc_db, args=(proc_id, execute_shell, os.getcwd())).start()

                os.chdir(wd)
                return proc_id

        os.chdir(wd)
        raise Exception(f'Not found action with extid {extid_action}')

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))


class HostService:

    def __init__(self, hostname: str, username: str, password: str, private_key: str):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.private_key = private_key

    def test_connection(self):
        try:
            ssh_client = paramiko.SSHClient()

            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)
            ssh_client.close()

            return True
        except Exception as e:
            logging.error(f'Try connet to host {self.hostname}, error: {e}')
            return False

    # Remove?
    def run_shell(self, command):
        params_ssh = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no '
        shell_execute = f'sshpass -p "{self.password}" ssh {params_ssh} {self.username}@{self.hostname} {command}'
        logging.info(f'run shell command {shell_execute}')
        return_code = subprocess.call(shell_execute, shell=True)

        return return_code
