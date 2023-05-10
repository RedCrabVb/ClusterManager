import logging

ORIGINS_WEB_APP = "http://localhost:4200"
INIT_FILES_DIR = "../../TmpConfigHadoop"
PROTOTYPE_INIT_FILES_DIR = "../../PrototypeTmpConfigHadoop"
CLUSTER_DIR = "../../TmpConfigHadoop/Cluster"
DB_NAME = "cm"
DB_USER = "cm_user"
DB_PASSWORD = "pass"
DB_HOST = "localhost"
DB_PORT = 34543
ENCODING_CONSOLE = "cp866"
expire_token = 1
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
record_filename_log = "../../record.log"
formate_log = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
level_log = logging.DEBUG
server_ai='http://localhost:5001/api/text'