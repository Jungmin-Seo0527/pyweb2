from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/menu')
def showMenu():
    db = sqlite3.connect("restaurant_menu.db")
    db.row_factory = sqlite3.Row
    items = db.execute(
        'select id, name, price, description from menu_item'
    ).fetchall()
    db.close()
    return render_template('menu.html', items= items)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)