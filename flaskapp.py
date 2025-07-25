from flask import Flask, request, render_template, redirect, url_for
from flask import jsonify
from flask_socketio import SocketIO, send, emit
from conversation import *
from os import listdir
import vector_database as vdb

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('QuerySubmitted', namespace='/chat')
def handle_query(message):
    print(f"Recieved: {message}")
    reply = answer_question(message['data'])
    for chunk in reply:
        print(chunk['message']['content'], end='', flush=True)
        emit(
            'ResponseReady',
            {'data':chunk['message']['content']},
            namespace='/chat'
        )

@app.route('/files')
def load_collection():
    name = request.args.get('name')
    print(f"Requested to load collection {name}")
    collection = vdb.load_collection(name)
    vdb.db_params['collection'] = collection
    file_list = []
    file_list.clear()
    for doc in collection.get(include=['metadatas'])['metadatas']:
        file_list.append(doc['title'])
    return jsonify(list(set(file_list)))

@app.route('/collections')
def available_collections():
    cols = vdb.list_collections()
    return jsonify(cols)

if __name__ == '__main__':
    socketio.run(app)