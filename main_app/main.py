import sys
from pathlib import Path

import uvicorn

import api

if __name__ == '__main__':
    print('Start ClusterManager')

    if not Path(api.PrototypeInitFilesDir).exists():
        Path(api.PrototypeInitFilesDir).mkdir()

    uvicorn.run(api.app, host=sys.argv[1], port=int(sys.argv[2]), log_level="info")


