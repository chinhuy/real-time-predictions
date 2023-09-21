import json
import random, math
from kafka import KafkaProducer
import os
import time

TOPIC = os.environ['TOPIC_INPUT']
INTERNAL_KAFKA_ADDR = os.environ['INTERNAL_KAFKA_ADDR']
KEY = 'exception'


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(ex)


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers=[INTERNAL_KAFKA_ADDR],
            api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(ex)
    return _producer


if __name__ == '__main__':

    kafka_producer = connect_kafka_producer()

    with open("movie-reviews.txt", "r+") as mfile:
        for line in mfile.readlines():
            message = {
                'review_id': str(math.floor(time.time()/1000)),
                'content': line.rstrip("\r\n"),
            }
            publish_message(kafka_producer, TOPIC, KEY, json.dumps(message))
            time.sleep(random.randint(1, 3))
        
        
    if kafka_producer is not None:
        kafka_producer.close()