from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/menu/edit/<int:menu_id>/', methods=['GET','POST'])
def editMenu(menu_id):
    if request.method=='POST':
        db = sqlite3.connect("restaurant_menu.db")
        db.row_factory = sqlite3.Row
        db.execute(
            'update menu_item'
            ' set name=?'
            ' where id=?',
            (request.form['menu_name'],menu_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('showMenu'))
    else:
        db = sqlite3.connect("restaurant_menu.db")
        db.row_factory = sqlite3.Row
        item = db.execute(
            'select id, name, price, description from menu_item where id=?',(menu_id,)
        ).fetchone()
        db.close()
        return render_template('editmenu.html', item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)