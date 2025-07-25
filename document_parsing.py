import chromadb
import pymupdf, pymupdf4llm
from chonkie import SemanticChunker
import pandas as pd
import os

def embed_with_metadata(doc_data: dict, db_params: dict)->None:
    client = db_params.get('client')
    collection = client.get_collection(
        name=db_params.get('collection')
    )
    chunk_data = {
        'ids':[],
        'documents':[],
        'metadatas':[]
    }
    text = doc_data['text']
    chunker = SemanticChunker()
    chunks = chunker(text)
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
    collection.add(**chunk_data)
        
def parse_pdf(filepath: str)->dict:
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

def parse_all_in_folder(path: str, db_params: dict)->None:
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            root, ext = os.path.splitext(filepath)
            if ext == '.pdf':
                print(f"Adding {filename} to database.")
                doc_data = parse_pdf(filepath)
                embed_with_metadata(doc_data, db_params)
            else:
                print(f"Filetype {ext} not supported.")




    
    


