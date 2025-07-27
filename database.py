import chromadb
import threading
from datetime import datetime
from document_parsing import *
import json

def list_collections():
    cols = []
    for collection in client.list_collections():
        cols.append({
            'name':collection.name,
            'count':collection.count()
        })
    return cols

def load_collection(name: str):
    print(f"Loading collection {name}")
    collection = client.get_collection(name)
    return collection

class DatabaseState:
    def __init__(self, DB_PATH: str, SETS_PATH: str):
        self.DB_PATH = DB_PATH
        self.SETS_PATH = SETS_PATH
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.db_params = {
            'path': DB_PATH,
            'client': self.client,
        }
        self.sets = self.load_sets_folder(SETS_PATH)
        if 'Empty_Set' in self.sets:
            self.active_set = self.sets['Empty_Set']
        else:
            Set = DocumentSet('Empty_Set', self.db_params)
            self.sets[Set.name] = Set
            self.active_set = Set

    def load_set(self, path: str)->DocumentSet:
        try:
            with open(path, "r") as f:
                load_dict = json.load(f)
                load_dict['db_params']=self.db_params
                Set = DocumentSet(**load_dict)
                return Set
        except Exception as e:
            print(e)        

    def load_sets_folder(self, path: str)->dict:
        sets = {}
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                root, ext = os.path.splitext(filepath)
                if ext == '.json':
                    print(f"Loading Document Set {filename}")
                    Set = self.load_set(filepath)
                    sets[Set.name] = Set
        print("All document sets loaded.")
        return sets

    def save_all_sets(self):
        for name, Set, in sets.items():
            Set.save(f"{self.SETS_PATH}/{Set.name}.json")

    def add_folder_thread(self, path: str, Set: DocumentSet):
        Set.add_folder(path)
        Set.save(self.SETS_PATH+"/"+"Test_Set.json")

    def add_folder(self, path: str, set_name: str):
        Set = self.sets[set_name] 
        thrd = threading.Thread(target=self.add_folder_thread, args=[path, Set])
        thrd.start()
