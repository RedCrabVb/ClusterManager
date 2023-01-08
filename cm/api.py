import paramiko
from ping3 import ping
from fastapi import FastAPI

app = FastAPI()

# return cluster
# return host
# return cluster example
# change params cluster example action
# run action
# create cluster from template

@app.get("/")
async def read_root():
    return {"Hello": "World"}
