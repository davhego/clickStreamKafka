import pymongo
import pandas as pd
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://clickStream:2Svqk4z7q6w8@proyectokafka.apfib.mongodb.net/?retryWrites=true&w=majority&appName=proyectoKafka"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clickStream']  # Nombre de tu base de datos
collection = db['tbl_loginxxx']  # Nombre de tu colección

# Obtener los datos de la colección
data = list(collection.find({}, {"email": 1, "fecha": 1, "_id": 0}))

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Asegurarse de que la columna 'fecha' esté en formato datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Contar correos por fecha
df_grouped = df.groupby(['fecha', 'email']).size().reset_index(name='conteo')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout del dashboard
app.layout = html.Div([
    html.H1("Conteo de Correos por Fecha"),
    dcc.Graph(id='grafico-correos')
])

# Definir la callback para actualizar el gráfico
@app.callback(
    Output('grafico-correos', 'figure'),
    [Input('grafico-correos', 'id')]
)
def actualizar_grafico(_):
    # Crear la gráfica
    figura = {
        'data': [
            {
                'x': df_grouped['fecha'],
                'y': df_grouped['conteo'],
                'type': 'bar',
                'name': 'Correos por Fecha'
            }
        ],
        'layout': {
            'title': 'Cantidad de Correos por Fecha'
        }
    }
    return figura

# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
