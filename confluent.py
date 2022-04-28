import json
import os

from executor import execute, ExternalCommandFailed
from typing import Dict, Optional, Tuple

ENV_LOGIN_EMAIL = "CONFLUENT_CLOUD_EMAIL"
ENV_LOGIN_PASSWORD = "CONFLUENT_CLOUD_PASSWORD"


def login() -> None:
    if ENV_LOGIN_EMAIL not in os.environ or ENV_LOGIN_PASSWORD not in os.environ:
        print(f"Please provide enviroment variables {ENV_LOGIN_EMAIL} and {ENV_LOGIN_PASSWORD}.")
        exit(0)
    execute("confluent login")


def logout() -> None:
    execute("confluent logout")


def list_envs() -> Tuple:
    return _list("environment")


def use_env(name: str) -> Optional[str]:
    env_id = _get_env_id_by_name(name)
    execute(f"confluent environment use {env_id}")
    return env_id


def list_clusters(environment: Optional[str] = None) -> Tuple:
    if environment:
        use_env(environment)
    return _list("kafka cluster")


def use_cluster(name: str) -> Optional[str]:
    cluster_id = _get_cluster_id_by_name(name)
    execute(f"confluent kafka cluster use {cluster_id}")
    return cluster_id


def list_topics(cluster: str) -> Dict:
    cluster_id = _get_cluster_id_by_name(cluster)
    res = execute(f"confluent kafka topic list --cluster {cluster_id} --output json", capture=True)
    return json.loads(res)


def create_topic(name: str, cluster: str, number_of_partitions: int = 3, config: Optional[Dict] = None) -> None:
    cluster_id = _get_cluster_id_by_name(cluster)
    cmd = f"confluent kafka topic create {name} --cluster {cluster_id} --partitions {number_of_partitions}"
    if config is not None and isinstance(config, type({})):
        cmd += " --config="
        cmd += ",".join([f"{k}={v}" for k, v in config.items()])
    try:
        execute(cmd, capture=True)
    except ExternalCommandFailed:
        pass


def delete_topic(name: str, cluster: str) -> None:
    cluster_id = _get_cluster_id_by_name(cluster)
    try:
        execute(f"confluent kafka topic delete {name} --cluster {cluster_id}")
    except ExternalCommandFailed:
        pass


def list_service_accounts() -> Dict:
    return _list("iam service-account")


def create_service_account(name: str, description: str) -> None:
    try:
        execute(f"confluent iam service-account create {name} --description \"{description}\"", capture=True)
    except ExternalCommandFailed:
        pass


def delete_service_account(name: str) -> None:
    service_account_id = _get_service_account_id_by_name(name)
    try:
        execute(f"confluent iam service-account delete {service_account_id}")
    except ExternalCommandFailed:
        pass


def _get_id_by_name(name, list_fn):
    resources = list_fn()
    for resource in resources:
        if resource.get("name") == name:
            return resource["id"]
    return None


def _get_env_id_by_name(name: str) -> str:
    return _get_id_by_name(name, list_envs)


def _get_cluster_id_by_name(name: str) -> str:
    return _get_id_by_name(name, list_clusters)


def _get_service_account_id_by_name(name: str) -> str:
    return _get_id_by_name(name, list_service_accounts)


def _list(resource):
    res = execute(f"confluent {resource} list --output json", capture=True)
    if not res:
        return None
    return json.loads(res)
