from kafka import KafkaProducer
import json
import time

def send_clickstream_event(producer, topic):
    # Obtener la hora actual en formato struct_time
    local_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    # Simulamos un evento de clickstream
    event = {
        'user_id': 'johan',
        'timestamp': formatted_time,
        'page': '/home',
        'action': 'click',
        'element': 'button_1'
    }
    # el value= realiza una asignación explicita al value_serializer
    producer.send(topic, value=event)
    print(f"Sent: {event}")

def conversion(valor):
    return json.dumps(valor).encode('utf-8');

if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        #lambad funcion es como los arrow funcions (variable)=> variable
        value_serializer= conversion
    )
    
    topic = 'clickstream-topic'
    
    while True:
        send_clickstream_event(producer, topic)
        time.sleep(3)  # Envía un evento cada 2 segundos
