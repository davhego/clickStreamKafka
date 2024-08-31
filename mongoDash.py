import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import plotly.express as px

# Conectar a MongoDB
uri = "mongodb+srv://clickStream:2Svqk4z7q6w8@proyectokafka.apfib.mongodb.net/?retryWrites=true&w=majority&appName=proyectoKafka"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    db = client['clickStream']  # Nombre de tu base de datos
    collection = db['tbl_usergold']  # Nombre de tu colección

    # Obtener los datos de la colección
    data = list(collection.find({}, {"username": 1, "fecha": 1, "_id": 0}))

    # Convertir los datos a un DataFrame
    df = pd.DataFrame(data)

    # Convertir la columna 'fecha' a formato datetime y eliminar la hora
    df['fecha'] = pd.to_datetime(df['fecha']).dt.date

    # Agrupar por fecha y username, contar cuántas veces se repite cada username por día
    df_grouped_username = df.groupby(['fecha', 'username']).size().reset_index(name='conteo_username')
    
    client.close()
except Exception as e:
    print(e)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout del dashboard
app.layout = html.Div([

    html.H1("Resumen de Datos",style={'text-align':'center'}),

    html.Div([
        html.Div([
            html.H4("Total de Registros"),
            html.P(str(df_grouped_username['conteo_username'].sum())),
        ], style={
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'padding': '10px',
            'width': '200px',
            'textAlign': 'center',
            'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
            'margin': '10px',
            'backgroundColor': '#f9f9f9'
        }),

        html.Div([
            html.H4("Username con Más Registros"),
            html.P(df_grouped_username.loc[df_grouped_username['conteo_username'].idxmax(), 'username']),
        ], style={
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'padding': '10px',
            'width': '200px',
            'textAlign': 'center',
            'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
            'margin': '10px',
            'backgroundColor': '#f9f9f9'
        })
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-around'
    }),

    html.H1("Conteo de Registros de Username por Fecha",style={'text-align':'center'}),
    
    # Gráfico de barras para el conteo de registros por username y fecha
    dcc.Graph(id='grafico-conteo-username'),

    # Gráfico de circular
    dcc.Graph(id='grafico-circular')

])

# Callback para actualizar el gráfico de conteo de registros por username
@app.callback(
    Output('grafico-conteo-username', 'figure'),
    [Input('grafico-conteo-username', 'id')]
)
def actualizar_grafico_conteo_username(_):
    fig = px.bar(df_grouped_username, x='fecha', y='conteo_username', color='username', barmode='group',
                 title='Conteo de Registros por Fecha y Username',
                 labels={'conteo_username': 'Cantidad de Registros', 'fecha': 'Fecha'})
    return fig

# Callback para actualizar el gráfico circular
@app.callback(
    Output('grafico-circular', 'figure'),
    [Input('grafico-circular', 'id')]
)
def actualizar_grafico_circular(_):
    fig = px.pie(df_grouped_username, values='conteo_username', names='username',
                 title='Distribución de Registros por Username en una Fecha')
    return fig

# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)