
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://clickStream:2Svqk4z7q6w8@proyectokafka.apfib.mongodb.net/?retryWrites=true&w=majority&appName=proyectoKafka"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    #print("Pinged your deployment. You successfully connected to MongoDB!")
    #obtengo todas las bases de datos que existen en mi app
    """dbs = client.list_databases()

    for db in dbs:
        print(db)

    database = client.get_database("sample_mflix")

    print(f"---------------------------------------")

    collections = database.list_collections()
    for c in collections:
        print(c)

    print(f"---------------------------------------")

    collections_name = database.list_collection_names()
    for cn in collections_name:
        print(cn)

    print(f"---------------------------------------")
    users = database.get_collection("users")
    print(users)

    movies = database.get_collection("movies")
    # Query for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }
    movie = movies.find_one(query)
    print(movie)
    """
    database = client["clickStream"]
    collection = database["tbl_usuarios"]

    #document_list = [{"user":"david","deporte":"basket"},{"user":"fulvio","deporte":"badmington"}]
    #result=collection.insert_many(document_list)


    datas = collection.find({})
    for data in datas:
        print(data)

    print(f"---------------------------------------")

    datas = collection.distinct("pais")
    for data in datas:
        print(data)

    print(f"---------------------------------------")
 
    """
    query_filter = {"user":"fulvio"}
    data_replace = {"pais":"colombia"}

    #replace_one remplaza el key y value del filtro aplicado una vez
    result = collection.replace_one(query_filter,data_replace)

    datas = collection.find({})
    for data in datas:
        print(data)

    
    result=collection.insert_one({"user":"johan"})
    print(result)
    print(result.acknowledged)
    print(result.inserted_id)

    document_list = [{"user":"jeison"},{"user":"lizi"}]
    result=collection.insert_many(document_list)
    print(result)
    print(result.acknowledged)
    print(result.inserted_ids)
    
    #Esta función me mostrará en pantalla todos lo cambios que se estan llevando a cabo sobre la base de datos
    with collection.watch() as stream:
        for change in stream:
            print(change)

    
    """

    client.close()

except Exception as e:
    print(e)