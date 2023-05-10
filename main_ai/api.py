from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

import config

origins = [
    config.ORIGINS_WEB_APP,
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)


@app.get('/api/text')
def add_task(context: str, text: str):
    import json
    import urllib.request

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Yandex',
        'Origin': 'https://russiannlp.github.io',
        'Referer': 'https://russiannlp.github.io',
    }
    API_URL = 'https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict'
    payload = {"text": 'Контекст: ---' + context + '\n---\n\n\n Вопрос: ' + text}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)

    return json.loads(urllib.request.urlopen(req).read(100000).decode('utf8'))
