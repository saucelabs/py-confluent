import confluent

confluent.login()
result = confluent.list_envs()
print("List envs: ", result)

result = confluent.use_env("saucelabs")
print("Used env: ", result)

result = confluent.list_clusters("saucelabs")
print(f"Found {len(result)} clusters")

result = confluent.use_cluster("staging-us-headless")
print("Used cluster: ", result)

result = confluent.list_topics("staging-us-headless")
print(f"Found {len(result)} topics")

confluent.create_topic("confluent-cli-test-topic", "staging-us-headless")

result = confluent.list_service_accounts()
print(f"Found {len(result)} service accounts")

confluent.create_service_account("confluent-cli-test-sa", "to be deleted")
confluent.create_topic_acl("confluent-cli-test-sa", "confluent-cli-test-topic", "READ", prefix=True)
confluent.create_consumer_group_acl("confluent-cli-test-sa", "confluent-cli-test-cg", "READ")

result = confluent.list_api_keys()
print(f"Found {len(result)} API keys")

result = confluent.create_api_key("staging-us-headless", "confluent-cli-test-sa")
print("Got a new key: ", result)

schema = {"properties": {"value": {"title": "Value", "type": "string"}}, "required": ["value"], "title": "TestTopic", "type": "object"}
confluent.create_schema("confluent-cli-test-topic", schema)
result = confluent.list_schemas("confluent-cli-test-topic")
print(f"Found {len(result)} schemas")

confluent.delete_schema("confluent-cli-test-topic")
confluent.delete_api_key(result["key"])
confluent.delete_consumer_group_acl("confluent-cli-test-sa", "confluent-cli-test-cg", "READ")
confluent.delete_topic_acl("confluent-cli-test-sa", "confluent-cli-test-topic", "READ", prefix=True)
confluent.delete_topic("confluent-cli-test-topic", "staging-us-headless")
confluent.delete_service_account("confluent-cli-test-sa")


confluent.logout()
