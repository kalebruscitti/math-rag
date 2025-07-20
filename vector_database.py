import chromadb
from datetime import datetime
from document_parsing import *

## https://docs.trychroma.com/docs/run-chroma/persistent-client

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

client = chromadb.PersistentClient(path=DB_PATH)
init_database(client)
collection_name = "TestCollection"
collection = client.get_collection(collection_name)

db_params = {
    'client': client,
    'collection': collection_name
}

#parse_all_in_folder('pdfs', db_params)
collection.query(
    query_texts=["marginal likelihood"]
)