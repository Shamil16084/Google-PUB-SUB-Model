import json
import re
import time
from google.cloud import pubsub_v1


SUBSCRIBER_ID = "1"
PROJECT_ID = "inft-3507"
TOPICS = ["INFO-shamil", "WARN-shamil", "ERROR-shamil", "DEBUG-shamil", "ALERT-shamil"]
RULES_FILE = "../config/rules.json"     
RULES_RELOAD_INTERVAL = 10               # seconds


def load_rules():
    """Load and compile regex rules for this subscriber"""
    with open(RULES_FILE, "r") as f:
        data = json.load(f)
    subscriber_rules = data["subscribers"][SUBSCRIBER_ID]
    compiled_rules = []
    for rule in subscriber_rules:
        compiled_rules.append({
            "level": rule["level"],
            "pattern": re.compile(rule["pattern"])
        })
    return compiled_rules

def matches_rules(message_text, message_level, rules):
    """Check if message matches any rule"""
    for rule in rules:
        if rule["level"] == message_level and rule["pattern"].search(message_text):
            return True
    return False

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscriptions = {}

    # Create subscriptions dynamically for each topic
    for topic in TOPICS:
        subscription_name = f"sub-{SUBSCRIBER_ID}-{topic}"
        topic_path = subscriber.topic_path(PROJECT_ID, topic)
        sub_path = subscriber.subscription_path(PROJECT_ID, subscription_name)

        try:
            subscriber.create_subscription(name=sub_path, topic=topic_path)
            print(f"Created subscription: {subscription_name}")
        except Exception:
            pass  # Subscription already exists

        subscriptions[topic] = sub_path

    # Load initial rules
    rules = load_rules()
    last_rules_load = time.time()

    def callback(message):
        nonlocal rules, last_rules_load

        # Reload rules dynamically 
        if time.time() - last_rules_load > RULES_RELOAD_INTERVAL:
            rules = load_rules()
            last_rules_load = time.time()
            print("Rules reloaded.")

        msg_data = message.data.decode("utf-8")
        msg_level = message.attributes.get("level", "")

        if matches_rules(msg_data, msg_level, rules):
            print(f"[{msg_level}] {msg_data}")

        message.ack()

    # Start listening to all subscriptions
    streaming_pull_futures = []
    for topic, sub_path in subscriptions.items():
        future = subscriber.subscribe(sub_path, callback=callback)
        streaming_pull_futures.append(future)
        print(f"Listening to {sub_path}...")

    try:
        for future in streaming_pull_futures:
            future.result()
    except KeyboardInterrupt:
        print("Subscriber stopped.")

if __name__ == "__main__":
    main()
