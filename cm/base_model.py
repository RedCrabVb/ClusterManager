from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenDataModel(BaseModel):
    username: str = None


class UserModel(BaseModel):
    username: str
    disabled: bool = None


class UserModelInDB(UserModel):
    hashed_password: str


class ItemInitFile(BaseModel):
    name: str
    namefile: str
    data: str


class ItemInitFileVersion(BaseModel):
    name: str
    version: str


class TaskRunAction(BaseModel):
    cluster: str
    extid_action: str
    intifle_name: str


class HostModel(BaseModel):
    hostname: str
    username: str
    password: str


class ItemAddClusterHost(BaseModel):
    name_cluster: str
    # host: HostModel
    group: str
    extid_service: str


class ClusterUserModel(BaseModel):
    name: str
    description: str
    initfile_name: str


class ClusterUpdateModel(BaseModel):
    cluster_name: str
    config_name: str
    config_file: str


class UpdateConfigItemModel(BaseModel):
    cluster_name: str
    config_name: str
    config_file: str


class RunActionModel(BaseModel):
    cluster_name: str
    extid: str
    extid_service: str
    shell_parameters: dict
