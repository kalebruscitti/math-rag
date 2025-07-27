from flask import Flask, request, render_template, redirect, url_for
from flask import jsonify
from flask_socketio import SocketIO, send, emit
from conversation import *
from os import listdir
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
DB_PATH = "./database"
SETS_PATH = "./sets"
socketio = SocketIO(app)
print("Initializing database.")
DB = DatabaseState(DB_PATH, SETS_PATH)
DB.add_folder('./pdfs', 'Test_Set')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('QuerySubmitted', namespace='/chat')
def handle_query(message):
    print(f"Recieved: {message}")
    reply = answer_question(message['data'], message['mode'], DB)
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
    file_list = []
    if name in DB.sets:
        DB.active_set = DB.sets[name]
        for doc in DB.active_set.documents:
            file_list.append(doc)
    else:
        print(f"Set {name} not found.")
    return jsonify(file_list)

@app.route('/collections')
def available_collections():
    return jsonify([
        {'name': doc_set.name, 'count': len(doc_set.documents)}
        for doc_set in DB.sets.values()
    ])

if __name__ == '__main__':
    socketio.run(app)