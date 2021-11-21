import datetime

import kubernetes as k
from dateutil.tz import tzutc


def _pods():
    k.config.load_kube_config()
    v1 = k.client.CoreV1Api()
    pods_results = v1.list_pod_for_all_namespaces(watch=False)
    return [
        x for x in pods_results.items if not x.metadata.namespace in ["kube-system", "local-path-storage"]
    ]


def _rule_template(n, v):
    return {"name": n, "valid": v}


def _image_prefix(pod):
    return all(
        x.image.split('/')[0] == "bitnami"
        for x in pod.spec.containers
    )


def _team_label_present(pod):
    labels = pod.metadata.labels
    return bool("team" in labels.keys() and labels["team"])


def _recent_start_time(pod):
    start_time = pod.status.start_time
    now = datetime.datetime.now(tz=tzutc())

    diff = (now - start_time).total_seconds()
    max_time = 60 * 60 * 24 * 7
    return diff < max_time


def _rule_eval(pod):
    return [
        _rule_template("image_prefix", _image_prefix(pod)),
        _rule_template("team_label_present", _team_label_present(pod)),
        _rule_template("recent_start_time", _recent_start_time(pod)),
    ]


def get_pods():
    return [
        {
            "pod": x.metadata.name,
            "rule_evaluation": _rule_eval(x)
        }
        for x in _pods()
    ]
