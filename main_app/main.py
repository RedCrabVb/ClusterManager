import sys
from pathlib import Path

import uvicorn

if __name__ == '__main__':
    print('Start ClusterManager')

    if not Path(main_app.cm.api.PrototypeInitFilesDir).exists():
        Path(main_app.cm.api.PrototypeInitFilesDir).mkdir()

    uvicorn.run(main_app.cm.api.app, host=sys.argv[1], port=int(sys.argv[2]), log_level="info")


