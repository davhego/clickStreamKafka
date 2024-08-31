import pymongo
import pandas as pd
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://clickStream:2Svqk4z7q6w8@proyectokafka.apfib.mongodb.net/?retryWrites=true&w=majority&appName=proyectoKafka"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
try:
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
    client.close()
except Exception as e:
    print(e)