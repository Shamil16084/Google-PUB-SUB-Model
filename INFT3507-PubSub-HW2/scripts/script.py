import sys
from google.cloud import pubsub_v1

PROJECT_ID = "inft-3507"
TOPICS = ["INFO-shamil", "WARN-shamil", "ERROR-shamil", "DEBUG-shamil", "ALERT-shamil"]
SUBSCRIBERS = ["0", "1", "2", "3"]  # Subscriber IDs

def setup():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # Create topics
    for topic in TOPICS:
        topic_path = publisher.topic_path(PROJECT_ID, topic)
        try:
            publisher.create_topic(name=topic_path)
            print(f"Created topic: {topic}")
        except Exception:
            print(f"Topic already exists: {topic}")

    # Create subscriptions for each subscriber for all topics
    for sub_id in SUBSCRIBERS:
        for topic in TOPICS:
            sub_name = f"sub-{sub_id}-{topic}"
            topic_path = subscriber.topic_path(PROJECT_ID, topic)
            sub_path = subscriber.subscription_path(PROJECT_ID, sub_name)
            try:
                subscriber.create_subscription(name=sub_path, topic=topic_path)
                print(f"Created subscription: {sub_name}")
            except Exception:
                print(f"Subscription already exists: {sub_name}")

def teardown():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # Delete subscriptions first
    for sub_id in SUBSCRIBERS:
        for topic in TOPICS:
            sub_name = f"sub-{sub_id}-{topic}"
            sub_path = subscriber.subscription_path(PROJECT_ID, sub_name)
            try:
                subscriber.delete_subscription(subscription=sub_path)
                print(f"Deleted subscription: {sub_name}")
            except Exception:
                print(f"Subscription not found: {sub_name}")

    # Delete topics
    for topic in TOPICS:
        topic_path = publisher.topic_path(PROJECT_ID, topic)
        try:
            publisher.delete_topic(topic=topic_path)
            print(f"Deleted topic: {topic}")
        except Exception:
            print(f"Topic not found: {topic}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py [setup|teardown]")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "setup":
        setup()
    elif action == "teardown":
        teardown()
    else:
        print("Invalid option. Use 'setup' or 'teardown'.")
