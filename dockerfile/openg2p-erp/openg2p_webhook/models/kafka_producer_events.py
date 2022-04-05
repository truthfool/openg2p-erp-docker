from json import dumps
from kafka import KafkaProducer
from kafka.errors import KafkaError


def producer_events(webhook_data):
    try:
        producer_data = KafkaProducer(bootstrap_servers=['localhost:2181'],
                                      value_serializer=lambda x:
                                      dumps(x).encode('utf-8'))

        # Sending events to topics
        producer_data.send('erp-events', value=webhook_data)

    except KafkaError as e:
        print(e)
