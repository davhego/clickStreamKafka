from flask import Flask, render_template, request
from producer import Producer

app = Flask(__name__)

@app.route('/')
@app.route('/<variable>')
def home(variable=None):
    return render_template('login.html',valor=variable)

@app.errorhandler(404)
def paginaError(error):
    return render_template('notFound.html')

@app.route('/setData',methods=['POST'])
def getDate():
    if request.method == 'POST':
        person={
            'username': request.form['name'],
            'email': request.form['email'],
            'picture': request.form['picture'],
        }
        sendDataProducer(person)
        return f'información recibida correctamente'
    else:
        return f'Error'

def sendDataProducer(person):
    productor = Producer(informacion=person)
    productor.enviar()

if __name__ == '__main__':
    app.run(debug=True,port=80)
