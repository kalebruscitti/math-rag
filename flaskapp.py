from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, send, emit
from conversation import *

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

if __name__ == '__main__':
    socketio.run(app)