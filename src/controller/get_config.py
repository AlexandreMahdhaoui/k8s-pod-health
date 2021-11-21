import os
import kubernetes as k8s
import kubernetes.config


def get_config():
    kubernetes.config.load_kube_config()
