# py-confluent

![Language](https://img.shields.io/badge/language-python-green.svg)
[![Latest Release][release badge]][release]
[![Last Commit][commit badge]][commit]

Simple Python library wrapping the Confluent Cloud CLI v3

### Installation

```bash
pip install py-confluent-cli
```
### Usage example

Setup your Confluent Cloud credentials in environment variables:
```bash
export CONFLUENT_CLOUD_EMAIL=...
export CONFLUENT_CLOUD_PASSWORD=...
```

Login and execute action:
```python
import confluent
confluent.login()
confluent.list_clusters()
confluent.create_topic("myTopic", "myCluster")
```

### Documentation:

```python
confluent.login()
```
Logs in to Confluent Cloud account enabling usage of confluent.

```python
confluent.logut()
```
Logs out from Confluent Cloud account.

```python
confluent.list_envs()
```
Lists all available Confluent Cloud environments.

```python
confluent.list_clusters()
```
Lists all available clusters.

```python
confluent.use_env(name: str)
```
Start using environment by given name.

```python
confluent.use_cluster(name: str)
```
Start using cluster by given name.

```python
confluent.create_topic(
    name: str,
    cluster: str,
    number_of_partitions: int = 3,
    config: Optional[Dict] = None)
```
Creates topic with given name on a given cluster.
Number of partitions can be provided.
Config can be provided to fulfill the need of less used parameters: https://docs.confluent.io/confluent-cli/current/overview.html

```python
confluent.delete_topic(name: str, cluster: str)
``` 
Deletes topic with given name on a given cluster.

```python
confluent.create_service_account(name: str, description: str)
```
Creates a service account with a given name and description.

```python
confluent.list_service_accounts()
```
Lists all available service accounts

```python
confluent.delete_service_account(name: str)
```
Deletes a service account by name.

```python
confluent.create_topic_acl(
    service_account: str,
    topic: str,
    operation: str,
    prefix: bool = False)
```
Creates an ACL for a service account to perform given operation a topic.
Operation might be e.g. `READ`, `WRITE`, `DESCRIBE`
Set `prefix=True` if you want to give access to a family of topics.

```python
confluent.delete_topic_acl(
    service_account: str,
    topic: str,
    operation: str,
    prefix: bool = False)
```
Deletes operation's ACL for a service account to a topic.

```python
confluent.create_consumer_group_acl(
    service_account: str,
    consumer_group: str,
    operation: str,
    prefix: bool = False)
```
Creates ACL for a consumer group like `create_topic_acl` for topic.

```python
confluent.delete_consumer_group_acl(
    service_account: str,
    consumer_group: str,
    operation: str,
    prefix: bool = False)
```
Deletes operation's ACL for a service account to a consumer group.

### Contributing

We would love to have outside contributors chiming in supporting us finishing this. Please have a look at our [contribution guidelines](https://github.com/saucelabs/py-confluent/blob/main/CONTRIBUTING.md).

[commit]: https://github.com/saucelabs/py-confluent/commit/HEAD
[release]: https://github.com/saucelabs/py-confluent/releases/latest

[commit badge]: https://img.shields.io/github/last-commit/saucelabs/py-confluent.svg
[release badge]: https://img.shields.io/github/release/saucelabs/py-confluent.svg
