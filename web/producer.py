from kafka import KafkaProducer
import json

class Producer:

    def __init__(self, informacion, id):
        self.informacion = informacion
        self.key = id.encode('utf-8')
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            #lambda funcion es como los arrow funcions (variable)=> variable
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    #metodo para enviar la data al consumer
    def enviar(self):
        topic = 'clickstream-topic'
        self.send_clickstream_event(self.producer, topic, self.informacion, self.key)

    def send_clickstream_event(self, producer, topic, event, id):
        # el value= realiza una asignación explicita al value_serializer
        print(f"Sent: {id}")
        producer.send(topic, value=event, key=id)
        print(f"Sent: {event}")
