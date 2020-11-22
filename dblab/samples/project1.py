from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
@app.route('/hello/<string:name>')
def hello(name=None):
    if name:
        return 'Hello {}!'.format(name)
    else:
        return "Hello World!"

@app.route('/goodbye')
@app.route('/goodbye/<string:name>')
def myfunc(name=None):
    if name:
        return 'Good bye {}!'.format(name)
    else:
        return "Good bye World!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)