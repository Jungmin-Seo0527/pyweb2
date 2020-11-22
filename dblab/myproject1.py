from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/hello/<string:name>')
def hello(name=None):
    if name != None:
        return 'Hello {}'.format(name)
    else:
        return "Hello World"


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
