import json
import os

from executor import execute, ExternalCommandFailed
from typing import Dict, Optional, Tuple

TITLE_ROWS_INDEX = 1
REQUIRED_ROWS_LENGTH = 2
ENV_LOGIN_EMAIL = "CONFLUENT_CLOUD_EMAIL"
ENV_LOGIN_PASSWORD = "CONFLUENT_CLOUD_PASSWORD"


###########
# API
###########


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
    execute(f"confluent kafka cluster use '{cluster_id}'")
    return cluster_id


def list_topics(cluster: str) -> Dict:
    cluster_id = _get_cluster_id_by_name(cluster)
    res = execute(f"confluent kafka topic list --cluster '{cluster_id}' --output json", capture=True)
    return json.loads(res)


def create_topic(name: str, cluster: str, number_of_partitions: int = 3, config: Optional[Dict] = None) -> None:
    cluster_id = _get_cluster_id_by_name(cluster)
    cmd = f"confluent kafka topic create '{name}' --cluster '{cluster_id}' --partitions {number_of_partitions}"
    if config is not None and isinstance(config, type({})):
        cmd += " --config="
        cmd += ",".join([f"{k}={v}" for k, v in config.items()])
    try:
        execute(cmd, capture=True, capture_stderr=True)
    except ExternalCommandFailed as exc:
        if _already_exists(exc):
            return
        raise


def _already_exists(exc: ExternalCommandFailed) -> bool:
    return "already exists" in str(exc.args).lower()


def delete_topic(name: str, cluster: str) -> None:
    cluster_id = _get_cluster_id_by_name(cluster)
    try:
        execute(f"confluent kafka topic delete '{name}' --cluster '{cluster_id}' --force")
    except ExternalCommandFailed:
        raise


def list_service_accounts() -> Dict:
    return _list("iam service-account")


def create_service_account(name: str, description: str) -> None:
    try:
        execute(f"confluent iam service-account create '{name}' --description \"{description}\"", capture=True)
    except ExternalCommandFailed:
        raise


def delete_service_account(name: str) -> None:
    service_account_id = _get_service_account_id_by_name(name)
    try:
        execute(f"confluent iam service-account delete '{service_account_id}' --force")
    except ExternalCommandFailed:
        pass


def create_topic_acl(service_account: str, topic: str, operation: str, prefix: bool = False) -> None:
    _acl(service_account, topic, operation, "topic", "create", prefix=prefix)


def delete_topic_acl(service_account: str, topic: str, operation: str, prefix: bool = False) -> None:
    _acl(service_account, topic, operation, "topic", "delete", prefix=prefix, force=True)


def create_consumer_group_acl(service_account: str, consumer_group: str, operation: str, prefix: bool = False) -> None:
    _acl(service_account, consumer_group, operation, "consumer-group", "create", prefix=prefix)


def delete_consumer_group_acl(service_account: str, consumer_group: str, operation: str, prefix: bool = False) -> None:
    _acl(service_account, consumer_group, operation, "consumer-group", "delete", prefix=prefix, force=True)


def list_api_keys() -> Dict:
    return _list("api-key")


def create_api_key(cluster: str, service_account: str) -> Dict:
    cluster_id = _get_cluster_id_by_name(cluster)
    service_account_id = _get_service_account_id_by_name(service_account)
    cmd = f"confluent api-key create --resource '{cluster_id}' --service-account '{service_account_id}' --output json"
    res = execute(cmd, capture=True)
    return json.loads(res)


def delete_api_key(api_key: str) -> None:
    try:
        execute(f"confluent api-key delete '{api_key}' --force")
    except ExternalCommandFailed:
        pass

###########
# HELPERS
###########


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


def _acl(service_account: str, resource_name: str, operation: str, resource: str, action: str, prefix: bool = False, force: bool = False):
    service_account_id = _get_service_account_id_by_name(service_account)
    cmd = f"confluent kafka acl '{action}' "
    cmd += f"--allow --service-account '{service_account_id}' --operations '{operation}' --{resource} '{resource_name}'"
    if prefix:
        cmd += " --prefix"
    if force:
        cmd += " --force"
    try:
        execute(cmd)
    except ExternalCommandFailed:
        raise
