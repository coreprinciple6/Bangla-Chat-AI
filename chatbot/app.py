from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from config import get_configurataion
from models.llm import LLModel
from models.embedding_generator import EmbeddingGenerator


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# configs = get_configurataion()
# pinecone = EmbeddingGenerator(configs)
#     # create embeddings
# vectorstore  = pinecone.create_embeddings()
# print(pinecone.get_index_stats())

# AI = LLModel(configs, vectorstore)


# @app.route('/')
# def index():
#     return render_template('chat.html')  # This will be your chat frontend

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     message = request.form['message']
#     print('received query: ' + message)
#     # Use LLM instance to get a response
#     response = AI.get_response(message)
#     print('response: ' + response)
#     response_data = {
#         'response': response  # Replace this with your actual LLM response
#     }

#     response_json = json.dumps(response_data, ensure_ascii=False)
#     return Response(response_json, content_type='application/json; charset=utf-8')
#    # emit('AI message', response, broadcast=True)
#     #return jsonify({'response': response}),  200, {'ContentType':'application/json; charset=utf-8'}


# @socketio.on('send_message')
# def handle_message(message):
#     # Process the message and emit a response
#     response = AI.get_response(message)
#     emit('receive_message', {'response': response})


# if __name__ == '__main__':
#     socketio.run(app, debug=True)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

configs = get_configurataion()
pinecone = EmbeddingGenerator(configs)
# create embeddings
vectorstore  = pinecone.create_embeddings()
print(pinecone.get_index_stats())

AI = LLModel(configs, vectorstore)

@app.route('/')
def index():
    return render_template('chat.html')  # Chat frontend


@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    response = AI.get_response(message)
    print('response: ' + response)
    emit('receive_message', {'response': response})

if __name__ == '__main__':
    socketio.run(app, debug=True)