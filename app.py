from flask import Flask
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)
leituras = []

@socketio.on('connected', namespace='/test')
def conncetedHandle():
    print("connected")
    return "200"

@app.route('/')
def hello_world():
    html = "<html><head><script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script><script src='https://cdn.socket.io/2.3.0/socket.io.min.js'></script></head><body><h1>Sensores Cadastrados:</h1>"
    
    if len(leituras) != 0:
        html += "<ul>"
        for s in leituras:
            html += "<li>" + s["sid"] + ": " + s["v"] + "</li>"
        html += "</ul>"
    else:
        html += "<p>Sem sensores cadastrados</p>"
    html += "</body><script>$(document).ready(function(){var socket = io.connect('http://127.0.0.1:5000/test');socket.on('newValue', function(obj) {console.log(obj);});})</script></html>"
    return html

@app.route('/leitura/<sid>/<valor>', methods=['POST'])
def lerSensor(sid, valor):
    yes = False
    index = 0
    if len(leituras) != 0:
        for s in leituras:
            if s["sid"] == sid:
                yes = True
            else: 
                index += 1
    if yes:
        leituras[index] = {"sid": sid, "v": valor}
    else:
        leituras.append({"sid": sid, "v": valor})
    socketio.emit('newValue', {"sid": sid, "v": valor})
    return "200"

