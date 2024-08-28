from kafka import KafkaProducer
import json
import time

def send_clickstream_event(producer, topic):
    # Simulamos un evento de clickstream
    event = {
        'user_id': 'user_123',
        'timestamp': int(time.time()),
        'page': '/home',
        'action': 'click',
        'element': 'button_1'
    }
    # el value= realiza una asignación explicita al value_serializer
    producer.send(topic, value=event)
    print(f"Sent: {event}")

if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        #lambad funcion es como los arrow funcions (variable)=> variable
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    topic = 'clickstream-topic'
    
    while True:
        send_clickstream_event(producer, topic)
        time.sleep(2)  # Envía un evento cada 2 segundos
