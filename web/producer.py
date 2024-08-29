from kafka import KafkaProducer
import json
import time

class Producer:

    def __init__(self, informacion):
        self.informacion = informacion
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            #lambda funcion es como los arrow funcions (variable)=> variable
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def enviar(self):
        topic = 'clickstream-topic'
        self.send_clickstream_event(self.producer, topic, self.informacion)

    def send_clickstream_event(self, producer, topic, event):
        # Simulamos un evento de clickstream
        #event = {
        #    'user_id': 'user_123',
        #    'timestamp': int(time.time()),
        #    'page': '/home',
        #    'action': 'click',
        #   'element': 'button_1'
        #}
        # el value= realiza una asignación explicita al value_serializer
        producer.send(topic, value=event)
        print(f"Sent: {event}")
