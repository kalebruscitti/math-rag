import chromadb
from datetime import datetime
from document_parsing import *

DB_PATH = "./database"

def init_database(client)->None:
    try:
        collection = client.create_collection(
            name = "TestCollection",
            metadata={
                "description": "Temporary collection.",
                "created": str(datetime.now())
            }
        )
    except Exception as e:
        print(e)

def list_collections():
    cols = []
    for collection in client.list_collections():
        cols.append({
            'name':collection.name,
            'count':collection.count()
        })
    return cols

def load_collection(name):
    print(f"Loading collection {name}")
    collection = client.get_collection(name)
    return collection


client = chromadb.PersistentClient(path=DB_PATH)
init_database(client)
collection_name = "TestCollection"
collection = client.get_or_create_collection(
    name=collection_name,
)

db_params = {
    'client': client,
    'collection': collection_name
}

#parse_all_in_folder('pdfs', db_params)