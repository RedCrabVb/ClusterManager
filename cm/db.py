# todo: connect to postgres, postgres continue table

import psycopg2
conn = psycopg2.connect(dbname='cm', user='cm_user',
                        password='pass', host='localhost', port='34543')

db = {
    'hosts': [
  {
    "hostname": "gdas",
    "username": "d",
    "password": "d",
    "status_connect": False
  },
  {
    "hostname": "asdg",
    "username": "dasd",
    "password": "dd",
    "status_connect": False
  }
],
    'init_files': [
        {
            "version": "v0",
            "namefile": "hadoop-ansible.zip",
            "name": "hadoop"
        }
    ],
    'clusters': [
        {
            "name": "d",
            "description": "d",
            "item": {
                "version": "v0",
                "namefile": "hadoop-ansible.zip",
                "name": "hadoop"
            },
            "data": [
                {
                    "action_vars": {

                    },
                    "actions": [
                        {
                            "extid": "etc_hosts_update",
                            "name": "Add info about hosts to /etc/hosts",
                            "params": None,
                            "shell": "ansible-playbook -i hosts/host network.yml"
                        },
                        {
                            "extid": "copy_file_hadoop",
                            "name": "Copy hadoop from local FS",
                            "params": None,
                            "shell": "sshpass -p {password_master} scp  -o StrictHostKeyChecking=no {download_path_with_file} {username_master}@{hostname_master}:{download_path}"
                        },
                        {
                            "extid": "download_from_server",
                            "name": "Download hadoop from URL",
                            "params": None,
                            "shell": "wget {remote_server_uri} -d {download_path}"
                        }
                    ],
                    "extid": "INIT_HADOOP",
                    "files_vars": {

                    },
                    "hosts": [

                    ],
                    "name": "Init service hadoop",
                    "requirements_groups": None,
                    "vars_service": [
                        {
                            "description": [
                                "download_path_with_file",
                                "username_master",
                                "hostname_master",
                                "password_master",
                                "download_path"
                            ],
                            "extid": "copy_file_hadoop",
                            "file": None,
                            "type": "action"
                        },
                        {
                            "description": [
                                "remote_server_uri",
                                "download_path"
                            ],
                            "extid": "download_from_server",
                            "file": None,
                            "type": "action"
                        }
                    ]
                },
                {
                    "action_vars": {

                    },
                    "actions": [
                        {
                            "extid": "install_master",
                            "name": "Install master",
                            "params": None,
                            "shell": "ansible-playbook -i hosts/host master.yml"
                        },
                        {
                            "extid": "install_worker",
                            "name": "Install worker",
                            "params": None,
                            "shell": "ansible-playbook -i hosts/host workers.yml -e \"master_ip={master_ip} master_hostname={master_hostname}\""
                        },
                        {
                            "extid": "add_host_TODO",
                            "name": "Add hosts",
                            "params": None,
                            "shell": "config hosts change; install worker"
                        }
                    ],
                    "extid": "HDFS_INSTALL",
                    "files_vars": {

                    },
                    "hosts": [
                        {
                            "hostname": "d",
                            "username": "d",
                            "password": "d",
                            "group": "workers"
                        }
                    ],
                    "name": "Install hdfs",
                    "requirements_groups": [
                        {
                            "count": 1,
                            "quantity_max": 1,
                            "type_host": "master"
                        },
                        {
                            "count": 1,
                            "quantity_max": None,
                            "type_host": "workers"
                        }
                    ],
                    "vars_service": [
                        {
                            "description": [
                                "master_ip",
                                "master_hostname"
                            ]
                        }
                    ]

                }
            ]

        }
    ]
}


def add_init_file(name, namefile, version):
    # todo: path FS
    db.get('init_files').append({"name": name, "namefile": namefile, "version": version})
