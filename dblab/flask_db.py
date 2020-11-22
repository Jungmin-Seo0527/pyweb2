from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello():
    db = sqlite3.connect("restaurant_menu.db")
    db.row_factory = sqlite3.Row
    items = db.execute(
        'SELECT name, price, description FROM menu_item'
    ).fetchall()
    output = ''
    for item in items:
        output += item['name']+'<br>'
        output += item['price']+'<br>'
        output += item['description']+'<br><br>'
    db.close()
    return output


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    db = sqlite3.connect("restaurant_menu.db")
    db.row_factory = sqlite3.Row

    items = db.execute(
        'SELECT id, name, price, description'
        ' FROM menu_item'
        ' WHERE restaurant_id=?', (restaurant_id,)
    ).fetchall()

    output = ''
    for item in items:
        output += item['name']+'<br>'
        output += item['price']+'<br>'
        output += item['description']+'<br>'
    db.close()
    return output


# template
@app.route('/template/')
@app.route('/template/<name>')
def temp(name=None):
    return render_template('hello2.html', name=name)


# templates db
@app.route('/restaurant2/<int:restaurant_id>/')
def restaurantMenu2(restaurant_id):
    db = sqlite3.connect('restaurant_menu.db')
    db.row_factory = sqlite3.Row

    restaurant = db.execute(
        'SELECT id, name FROM restaurant WHERE id=?', (restaurant_id,)
    ).fetchall()

    items = db.execute(
        'SELECT name, id, price, description'
        ' FROM menu_item WHERE restaurant_id=?', (restaurant_id,)
    ).fetchall()
    db.close()
    return render_template('menu2.html',
                           restaurant=restaurant, items=items)


# From requests
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    db = sqlite3.connect("restaurant_menu.db")
    db.row_factory = sqlite3.Row
    if request.method == 'POST':
        db.execute(
            'UPDATE menu_item SET'
            ' name=?'
            ' WHERE id=?',
            (request.form['name'], menu_id,)
        )
        db.commit()
        db.close()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        editedItem = db.execute(
            'SELECT *'
            ' FROM menu_item'
            ' WHERE id=?',
            (menu_id,)
        ).fetchone()
        db.close()
        return render_template(
            'editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id,
            item=editedItem
        )


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
