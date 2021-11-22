import json
import os

from json2html import *
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from src.controller.get_pods import get_pods
from src.install_pre_req import install_pre_req

# install_pre_req()

os.system('kubectl apply -f ./k8s-pods-config/conform-pod.yaml >> logs.txt')
os.system('kubectl apply -f ./k8s-pods-config/wrong-pod.yaml >> logs.txt')

app = FastAPI()


@app.get("/")
def root():
    [print(x) for x in get_pods()]
    return HTMLResponse(
        content=json2html.convert(
            json=json.dumps(get_pods())
        )
    )


@app.get("/json")
def json_():
    [print(x) for x in get_pods()]
    return JSONResponse(
        content=json.dumps(get_pods())
    )


if __name__ == '__main__':
    [print(x) for x in get_pods()]

# pipenv run python -m main
# pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 30080
