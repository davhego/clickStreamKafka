from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from azure.storage.blob import BlobServiceClient
import json
import io

uri = "mongodb+srv://clickStream:2Svqk4z7q6w8@proyectokafka.apfib.mongodb.net/?retryWrites=true&w=majority&appName=proyectoKafka"

#conectamos con la api
client = MongoClient(uri,server_api=ServerApi('1'))
database = client["clickStream"]
collection = database["tbl_usergold"]

indices = collection.list_indexes()

# Verificar si el índice ya existe
indice_existe = any(indice['name'] == "nameFile" for indice in indices)
if indice_existe:
    collection.create_index("nameFile")

#conectamos con el servicio de azure
blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=espacio2;AccountKey=yDTeT0HDDthr9WSBh9E8vbFqDq1Md6zUiXjs1me5o0xbXlrQoSnmKxjKU6iWqVrxEW1liTz3UJ1x+AStTN9Nzw==;EndpointSuffix=core.windows.net')  # la cadena de conexión

def list_blobs(container_client, prefix):
    blobs = container_client.list_blobs(name_starts_with=prefix)
    return [blob.name for blob in blobs]

# Función para extraer datos de la capa Bronze
def extract_data(container_name, blob_name):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Descargar el blob como stream
    stream = io.BytesIO()
    blob_client.download_blob().readinto(stream)
    stream.seek(0)

    # Leer los datos en formato JSON y convertirlos en un DataFrame de pandas
    data = json.load(stream)  # Aquí cargamos el JSON
    return data

# Función para transformar los datos
def transform_data(df,blob_name):
    #all es una funcion que verifica que todas las condiciones para los iterables se cumplen.
    #cuando se cumple retorna True.
    if all(key in df for key in('username','email','fecha')):

        try:
            nuevoDiccionario = {
                "username":df["username"],
                "email":df["email"],
                "fecha":df["fecha"],
            }

            #Buscamos si ya existe el nombre del archivo en la collecion
            num_documents = collection.count_documents({"nameFile":blob_name})
            if num_documents == 0:
                return nuevoDiccionario
            else:
                return False
        
        except Exception as e:
            print(e)
            return False
    return False

# Función para cargar los datos en la capa Silver (en formato JSON)
def load_data(df, blob_name):
    # Convertir el DataFrame a JSON

    try:
        #Al diccionarioo de datos que me llega le agrego el nombre del archivo
        #para tenerlo presente al insertar
        df['nameFile'] = blob_name

        #insertamos el diccionario a la colección
        resultado = collection.insert_one(df)

        # Imprimir el ID del documento insertado
        print(f"Documento insertado con ID: {resultado.inserted_id}")

        
    except Exception as e:
        print(e)

# Ejecuta el pipeline ETL para todos los archivos en la carpeta Bronze
def run_etl():
    silver_container = "contenido23"  # nombre del contenedor Silver
    silver_folder = "silver/clickstream/"  # carpeta de la capa Bronze

    # Conectarse al contenedor Bronze
    container_client = blob_service_client.get_container_client(silver_container)

    # Listar todos los blobs en la carpeta Bronze
    blob_names = list_blobs(container_client, silver_folder)

    for blob_name in blob_names:

        # Extracción
        df = extract_data(silver_container, blob_name)

        # Transformación
        blob_name = blob_name.split("/")[-1]#obtenemos el nombre del archivo como tal
        df_transformed = transform_data(df,blob_name)

        # Carga
        if df_transformed :
            load_data(df_transformed, blob_name )
        else:
            continue

        print(f"ETL completado para {blob_name} y datos almacenados en Mongo!")
    #termina el ciclo for
    
    client.close()

if __name__ == "__main__":
    run_etl()