import uvicorn

import cm.api

if __name__ == '__main__':
    print('Start ClusterManager')
    uvicorn.run(cm.api.app, host="localhost", port=5000, log_level="info")


