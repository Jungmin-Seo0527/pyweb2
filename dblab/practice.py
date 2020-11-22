from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello"

# show restaurant list
@app.route('/restaurant/')
def showRestaurantList():
    db = sqlite3.connect('restaurant_menu.db')
    db.row_factory = sqlite3.Row
    restaurants = db.execute(
        'SELECT * FROM restaurant'
    ).fetchall()
    db.close()
    return render_template('showRes.html', restaurants=restaurants)


# show menu list
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    db = sqlite3.connect('restaurant_menu.db')
    db.row_factory = sqlite3.Row
    restaurant = db.execute(
        'SELECT name, id FROM restaurant WHERE id=?', (restaurant_id,)
    ).fetchall()
    items = db.execute('SELECT id, name, price, description'
                       ' FROM menu_item'
                       ' WHERE restaurant_id=?', (restaurant_id,)
                       ).fetchall()
    db.close()
    return render_template('showMenu.html', restaurant=restaurant, items=items)


# show about menu
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/')
def showAboutMenu(restaurant_id, menu_id):
    db = sqlite3.connect('restaurant_menu.db')
    db.row_factory = sqlite3.Row
    info = db.execute(
        'SELECT name, id, description, price, course From menu_item WHERE id=?', (
            menu_id,)
    ).fetchall()
    db.close()
    return render_template('showAboutMenu.html', item=info, restaurant_id=restaurant_id)


# edit menu info
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenu(restaurant_id, menu_id):
    db = sqlite3.connect('restaurant_menu.db')
    db.row_factory = sqlite3.Row
    if request.method == 'POST':
        db.execute(
            'UPDATE menu_item SET name=?, description=?, price=? WHERE id=?',
            (request.form['menu_name'], request.form['menu_description'],
             request.form['menu_price'], menu_id,)
        )
        db.commit()
        db.close()
        return redirect(url_for('showAboutMenu', restaurant_id=restaurant_id, menu_id=menu_id))

    else:
        editedItem = db.execute(
            'SELECT * FROM menu_item WHERE id=?', (menu_id,)
        ).fetchall()
        db.close()
        return render_template('editMenuInfo.html', restaurant_id=restaurant_id,
                               menu_id=menu_id, item=editedItem)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
