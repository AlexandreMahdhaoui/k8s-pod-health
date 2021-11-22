# Kubernetes Pod Evaluation Service
## Reproducible test environment
- Please ensure ``Vagrant`` and ``VirtualBox`` is installed on your machine.
- Open a terminal, ``cd`` to this directory and run ``vagrant up``. 
Please note this operation can take up to 10 minutes.
- You can now checkout the results in your **terminal** or:
  - `HTTP GET 10.10.10.21/`: Results displayed in a table.
  - `HTTP GET 10.10.10.21/json`: Results in JSON format.

### Vagrantfile
- Create a Centos:7 Virtual Machine
- Install Python 3.9, Docker, Kind
- Runs main.py
- Start server on port 80.

___

## Simple local test

### Install, run following commands in your terminal:
Please ensure ``kubectl`` is installed on your machine.
```shell
pip install pipenv
pipenv install
choco install kind
kind create cluster
```

If not running on a Windows machine, please replace ``choco`` by your package manager or install from source:
```shell
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind
```

### Printing results in terminal:
```shell
pipenv run python -m main
```

### Running evaluation from browser at GET ``localhost:30080``:
```shell
pipenv run uvicorn main:app --host 0.0.0.0 --port 30080
```


___

## Containered test (failed)

First go to ``/main.py`` and uncomment line **11**

Run the following command in terminal:
```shell
docker build -t k8s-pod-health . &&\
  docker run --privileged \
  -v //var/run/docker.sock:/var/run/docker.sock \
  --name k8s-pod-health -p 40080:40080 \
  --network host\
  k8s-pod-health
```

Setting up ``dind`` by biding ``docker.sock``in order to create
the `kind` cluster.

### However I'd need a bit more time to investigate 2 issues:
- First is connecting to ``localhost:40080`` when using ``--network host`` 
which is used because the ``.kube`` created by ``kind`` is referring to a ``localhost``.
- Experienced issues connecting to `default namespace` with default account when trying to deploy ``conform`` and ``wrong`` pods with ``kubectl``.