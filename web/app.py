from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<variable>')
def home(variable=None):
    return render_template('login.html',valor=variable)

@app.errorhandler(404)
def paginaError(error):
    return render_template('notFound.html')
if __name__ == '__main__':
    app.run(debug=True,port=80)
