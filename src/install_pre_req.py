import os


def _install_kind():
    try:
        if not os.name == 'nt':
            os.system('curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64 >> logs.txt')
            os.system('chmod +x ./kind >> logs.txt')
            os.system('mv ./kind /usr/local/bin >> logs.txt')
            os.system('kind create cluster >> logs.txt')
    except:
        try:
            os.system('kind delete cluster >> logs.txt')
        finally:
            os.system('kind create cluster >> logs.txt')


def _install_kubectl():
    os.system(
        'curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl >> logs.txt &&'
        'chmod +x ./kubectl >> logs.txt &&'
        'mv ./kubectl /usr/local/bin/kubectl >> logs.txt &&')


def install_pre_req():
    _install_kind()
