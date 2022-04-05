import requests
import json
from .kafka_producer_events import producer_events
from dicttoxml import dicttoxml
# from xml.dom.minidom import parseString


def webhook_event(webhook_data, webhook_url, type_data):
    print(webhook_data, webhook_url, type_data)
    print("Hello")
    headers = {}
    data = None

    if type_data == "JSON":
        headers['Content-Type'] = 'application/json'

        data = json.dumps(webhook_data)

    elif type_data == "XML":
        headers['Content-Type'] = 'application/xml'

        data = dicttoxml(webhook_data)
        # data = parseString(data)
    try:
        response = requests.post(webhook_url, data=data,
                                 headers=headers)

        # Sending to kafka topic
        producer_events(webhook_data)

    except BaseException as e:
        print(e)
