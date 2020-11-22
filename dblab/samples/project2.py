from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello():
    db = sqlite3.connect("restaurant_menu.db")
    db.row_factory = sqlite3.Row
    items = db.execute(
        'select name, price, description from menu_item'
    ).fetchall()
    output=''
    for item in items:
        output += item['name'] +'<br>'
        output += item['price'] +'<br>'
        output += item['description'] +'<br><br>'
    db.close()
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)