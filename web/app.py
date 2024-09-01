from flask import Flask, render_template, request
from producer import Producer
import time

app = Flask(__name__)

#Se crea una variable de ruta para recibir por medio de POST, la variable puede ser nula
@app.route('/')
@app.route('/<variable>')
def home(variable=None):
    return render_template('login.html',valor=variable)

#Si ocurre un error 404 se presnta un template aviso de notFound
@app.errorhandler(404)
def paginaError(error):
    return render_template('notFound.html')

#Defino la ruta para lectura por metodo POST de /setData
@app.route('/setData',methods=['POST'])
def getData():
    if request.method == 'POST':
        # Obtener la hora actual en formato año_mes_dia_H_m_s
        local_time = time.localtime()
        fecha = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        formatted_time = time.strftime("%Y_%m_%d__%H_%M_%S", local_time)
        #Defino el id o Key de mis datos
        id = f"{request.form['name']}_{formatted_time}"
        #Creo el diccionario
        person={
            'username': request.form['name'],
            'email': request.form['email'],
            'picture': request.form['picture'],
            'fecha': fecha
        }
        sendDataProducer(person, key=id)
        return f'información recibida correctamente'
    else:
        return f'Error'

#Función para enviar la información por medio del broker Kafka
def sendDataProducer(person,key):
    key = key.replace(" ","_")
    productor = Producer(informacion=person, id=key)
    productor.enviar()

if __name__ == '__main__':
    app.run(debug=True,port=80)
