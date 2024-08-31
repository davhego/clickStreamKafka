
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

# Leer el archivo JSON
with open('./bd/data.json', 'r') as file:
    data = json.load(file)

uri = "mongodb+srv://clickStream:2Svqk4z7q6w8@proyectokafka.apfib.mongodb.net/?retryWrites=true&w=majority&appName=proyectoKafka"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    result=client.admin.command('ping')

    print(result)

    database = client["clickStream"]
    collection = database["tbl_loginxxx"]

    # Insertar los datos
    #if isinstance(data, list):
    #    # Inserta una lista de documentos
    #    collection.insert_many(data)
    #else:
    #    # Inserta un solo documento
    #    collection.insert_one(data)  

    client.close()

except Exception as e:
    print(e)