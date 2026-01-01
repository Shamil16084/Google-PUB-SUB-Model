import csv
import time
from google.cloud import pubsub_v1


# Configuration

PROJECT_ID = "inft-3507"  
TOPIC_SUFFIX = "shamil"
CSV_FILE = "../logs.csv" 

# Initialize 
publisher = pubsub_v1.PublisherClient()


def get_topic_path(level: str) -> str:
    topic_name = f"{level.upper()}-{TOPIC_SUFFIX}"
    return publisher.topic_path(PROJECT_ID, topic_name)  # build full path


def main():
   
    with open(CSV_FILE, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        logs = list(reader)

    print(f"Loaded {len(logs)} log lines.")

    # Publish 
    while True:
        for log in logs:
            level = log["level"]
            message = log["message"]
            topic_path = get_topic_path(level)

            # Publish message publishes to a Pub/Sub topic (topic_path) , sending bytes, wait for confirmation.
            future = publisher.publish(topic_path, message.encode("utf-8"),level=level.upper())
            print(f"Published to {topic_path}: {message}")
            future.result()  

           
            time.sleep(2)

if __name__ == "__main__":
    main()
