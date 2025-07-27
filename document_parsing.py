import chromadb
import pymupdf, pymupdf4llm
from chonkie import SemanticChunker
import pandas as pd
from datetime import datetime
import os
import json

class DocumentSet:
    def __init__(self, name: str, db_params: dict, documents={}):
        self.name = name
        self.documents = documents
        self.db_params = db_params
        self.chunker = SemanticChunker()
        self.collection = self.initialize_collection()

    def initialize_collection(self):
        try:
            collection = self.db_params['client'].get_or_create_collection(
                name = self.name,
                metadata = {
                    "description":"",
                    "created": str(datetime.now())
                }
            )
            return collection
        except Exception as e:
            print(e)

    def add(self, filepath: str):
        doc_data = self.parse_pdf(filepath)
        if doc_data['file'] in self.documents:
            print(f"Skipping {doc_data['file']}, already in collection.")
            return 1
        print(f"Adding {doc_data['file']} to database.")
        chunk_data = {
            'ids':[],
            'documents':[],
            'metadatas':[]
        }
        text = doc_data['text']
        chunks = self.chunker(text)
        chunk_no = 0
        for chunk in chunks:
            chunk_data['ids'].append(f"{doc_data['title']}_{str(chunk_no)}")
            chunk_data['documents'].append(chunk.text)
            chunk_data['metadatas'].append({
                'file':doc_data['file'],
                'title':doc_data['title'],
                'length':chunk.token_count
            })
            chunk_no += 1
        # 
        self.documents[doc_data['file']] = {
            'title':doc_data['title'],
            'file':doc_data['file'],
            'added': str(datetime.now()),
            'chunks': chunk_no
        }
        self.collection.add(**chunk_data)
            
    def parse_pdf(self, filepath: str)->dict:
        document = pymupdf.open(filepath)
        if 'title' in document.metadata:
            title=document.metadata['title']
            if title == '':
                print(f"Warning: Blank title for {filepath}")
                title=filepath
        else:
            print(f"Warning: No title found for {filepath}")
            title=filepath

        doc_data = {
            'text':pymupdf4llm.to_markdown(document),
            'title':title,
            'file':filepath
        }
        return doc_data

    def add_folder(self, dirpath: str):
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                root, ext = os.path.splitext(filepath)
                if ext == '.pdf':
                    self.add(filepath)
                else:
                    print(f"Filetype {ext} not supported.")
        print("All files added!")

    def save(self, filepath: str):
        save_dict = {
            'name':self.name,
            'documents':self.documents,
        }
        print(f"Saving set {self.name} to {filepath}.")
        try:
            with open (filepath, 'w') as f:
                json.dump(save_dict, f)
        except Exception as e:
            print(e)

    
    


