import sys
from pathlib import Path

import uvicorn

import cm.api

if __name__ == '__main__':
    print('Start ClusterManager')

    if not Path(cm.api.PrototypeInitFilesDir).exists():
        Path(cm.api.PrototypeInitFilesDir).mkdir()

    uvicorn.run(cm.api.app, host=sys.argv[1], port=int(sys.argv[2]), log_level="info")


