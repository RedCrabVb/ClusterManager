import sys

import uvicorn

import api

if __name__ == '__main__':
    print("Api AI")

    print("context: all string")
    print("return other windows")

    print("AI: string context, return context + result")

    uvicorn.run(api.app, host=sys.argv[1], port=int(sys.argv[2]), log_level="info")


