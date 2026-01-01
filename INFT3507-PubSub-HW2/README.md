# Content-Based Subscription with Google Cloud Pub/Sub

## Overview

This project implements a content-based subscription system using Google Cloud Pub/Sub. The goal is to deliver messages to subscribers based on the **content of the message** (for example, log level and message patterns), even though Pub/Sub natively only supports topic-based subscriptions.

Each subscriber program listens to multiple topics and filters the messages based on **rules defined per subscriber**.



## Features

- **Publisher**: Reads log messages from a CSV file and publishes them to topics according to their log level (`INFO`, `WARN`, `ERROR`, `DEBUG`, `ALERT`).
- **Subscriber**: Listens to multiple topics, receives messages, and checks them against **regex-based rules**.
- **Dynamic Rule Loading**: Subscribers reload the filtering rules every 10 seconds without restarting.
- **Automated Topic and Subscription Management**: Scripts can create or delete all topics and subscriptions easily.



## Architecture

The system works as follows:

1. Publisher reads logs from `logs.csv`.
2. Publisher sends messages to corresponding Pub/Sub topics with a `level` attribute.
3. Each subscriber program has multiple subscriptions (one per topic).
4. Subscriber receives messages and applies rules based on log level and regex patterns.
5. Only messages that match the rules are processed (printed).

Example topics: `INFO-shamil`, `WARN-shamil`, `ERROR-shamil`, `DEBUG-shamil`, `ALERT-shamil`  
Example subscriptions for Subscriber 0: `sub-0-INFO-shamil`, `sub-0-WARN-shamil`, `sub-0-ERROR-shamil`, `sub-0-DEBUG-shamil`, `sub-0-ALERT-shamil`



## Setup

1. Make sure **Python 3.x** and **Google Cloud SDK** are installed.
2. Authenticate with Google Cloud:
    ```bash
    gcloud auth application-default login
    ```
3. Install the required Python package:
    ```bash
    pip install google-cloud-pubsub
    ```
4. (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    pip install google-cloud-pubsub
    ```



## Running the Project

### 1. Create Topics
Run the script to create all required topics and subscriptions.
```bash
python scripts/create_topics.py
```
2. Run Publisher
```bash
python publisher/publisher.py
```

3. Run Subscribers
```bash
Open separate terminals for each subscriber:
python subscribers/subscriber0.py
python subscribers/subscriber1.py
python subscribers/subscriber2.py
python subscribers/subscriber3.py
```
4. Update Rules Dynamically

Edit config/rules.json. Subscribers reload the rules automatically every 10 seconds.