from flask import Flask
from producer import publish
from consumer import start_consuming, channel
import threading

app = Flask(__name__)

t = threading.Thread(target=start_consuming)
t.start()

print(channel.is_closed)


@app.route('/')
def hello():
    if channel.is_closed:
        return 'channel close'
    if channel.is_open:
        body = {'message': 'hello world from producer'}
        publish('message-text', body)
        return '¡Hola, bienvenido al microservico con Flask!'


@app.route('/welcome/')
def welcome():
    return '¡bienvenido al microservico email con Flask!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=True)
