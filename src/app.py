from flask import Flask
from producer import publish
from consumer import start_consuming, channel
import threading

app = Flask(__name__)


t = threading.Thread(target=start_consuming)
t.start()


@app.route('/')
def hello():
    body = {'message': 'hello word from producer'}
    publish('message-text', body)
    return '¡Hola, bienvenido al microservico con Flask!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=True)
