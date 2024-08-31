from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json

# Configura el cliente de Azure Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=espacio2;AccountKey=yDTeT0HDDthr9WSBh9E8vbFqDq1Md6zUiXjs1me5o0xbXlrQoSnmKxjKU6iWqVrxEW1liTz3UJ1x+AStTN9Nzw==;EndpointSuffix=core.windows.net"  # Reemplaza con tu cadena de conexión
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

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
    df = pd.json_normalize(data)  # Convertimos el JSON a un DataFrame
    return df

# Función para transformar los datos
def transform_data(df):
    # Ejemplo de limpieza y transformación
    df.dropna(inplace=True)  # Eliminar filas con valores nulos
    df.drop_duplicates(inplace=True)  # Eliminar duplicados
    # Convertir a datetime si es necesario

    # Agregar más transformaciones según sea necesario
    return df

# Función para cargar los datos en la capa Silver (en formato JSON)
def load_data(df, container_name, output_blob_name):
    # Convertir el DataFrame a JSON
    output_json = df.to_json(orient='records', lines=True)

    # Subir los datos transformados al contenedor de la capa Silver
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(output_blob_name)
    blob_client.upload_blob(output_json, overwrite=True)

# Ejecuta el pipeline ETL para todos los archivos en la carpeta Bronze
def run_etl():
    bronze_container = "contenido23"  # nombre del contenedor Bronze
    silver_container = "contenido23"  # nombre del contenedor Silver
    bronze_folder = "bronze/clickstream/"  # carpeta de la capa Bronze

    # Conectarse al contenedor Bronze
    container_client = blob_service_client.get_container_client(bronze_container)

    # Listar todos los blobs en la carpeta Bronze
    blob_names = list_blobs(container_client, bronze_folder)

    for blob_name in blob_names:
        # Generar el nombre de salida para la capa Silver
        output_blob_name = "silver/clickstream/" + blob_name.split("/")[-1].replace(".json", "_silver.json")
        
        # Extracción
        df = extract_data(bronze_container, blob_name)

        # Transformación
        df_transformed = transform_data(df)

        # Carga
        load_data(df_transformed, silver_container, output_blob_name)

        print(f"ETL completado para {blob_name} y datos almacenados en {output_blob_name} en la Silver Layer")

if __name__ == "__main__":
    run_etl()