from pydantic import BaseModel

from cm.service import HostService


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    disabled: bool = None


class UserInDB(User):
    hashed_password: str


class ItemInitFile(BaseModel):
    name: str
    namefile: str
    data: str


class ItemInitFileVersion(BaseModel):
    name: str
    version: str


class ItemAddClusterHost(BaseModel):
    name_cluster: str
    host: HostService
    group: str
    extid_service: str


class TaskRunAction(BaseModel):
    # type: str # add_host cluster, test_connection, run_action,
    cluster: str
    extid_action: str
    intifle_name: str


class ClusterUser(BaseModel):
    name: str
    description: str
    initfile_name: str


class ClusterUpdate(BaseModel):
    cluster_name: str
    config_name: str
    config_file: str


class UpdateConfigItem(BaseModel):
    cluster_name: str
    config_name: str
    config_file: str


class RunActionModel(BaseModel):
    cluster_name: str
    extid: str
    extid_service: str
    shell_parameters: dict