import os
import time
import json
import datetime
import numpy as np
import uuid
from pykafka import KafkaClient


class Rover:
    def __init__(self, name='default'):
        self.id = uuid.uuid4()
        self.NAV_PYT_Message = ['timestamp', 'coords', 'heading', 'velocity', 'accuracy']
        self.name = name
        self.message = dict.fromkeys(self.NAV_PYT_Message, 0)

        self.client = KafkaClient(hosts="localhost:9092")
        self.topic = self.client.topics['testFrontend']
        self.producer = self.topic.get_sync_producer()
        self.producer.produce(f'Rover {self.name} with id: {self.id} connected'.encode('ascii'))

    def stream_to_kafka(self):
        try:
            self.producer.produce(json.dumps(self.message).encode('ascii'))
        except:
            self.producer.flush()

    def parse_row(self, line):
        p = (10**-3) # mm -> m
        line.strip()
        d = json.loads(line.replace("'",'"'))
        if d['MessageType'] == 'NAV-PYT':
            time_seconds = int(datetime.datetime.strptime(' '.join([str(d['year']), 
                    str(d['month']), str(d['day']), str(d['hour']), str(d['min']), str(d['second'])]), 
                                                                '%Y %m %d %H %M %S').timestamp())
            self.message['timestamp'] = time_seconds
            self.message['coords'] = (d['lon'], d['lat'])
            self.message['heading'] = round(d['headMot'], 2)
            self.message['velocity'] = round(d['gSpeed']*p*3.6, 2)
            self.message['accuracy'] = (round(d['hAcc']*p, 2), round(d['vAcc']*p, 2))

            self.stream_to_kafka()


def read_GNSS(gnss_path, time_interval = 1):
    os.chdir(gnss_path)
    for file in [file for file in os.listdir() if file.endswith(".txt")]:
        with open(file, 'r') as f: # Equal to open connection
            rover = Rover(file[:6])
            while True:
                line = f.readline()
                if not line:
                    break
                print(line)
                rover.parse_row(line)
                time.sleep(time_interval)


path = "GeoticData"
read_GNSS(path, time_interval = 0.5)
