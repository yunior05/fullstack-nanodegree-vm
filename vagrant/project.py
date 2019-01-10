from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Create Session to Database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
@app.route("/")
@app.route("/restaurants/<int:restaurant_id>/")
def Restaurants(restaurant_id):
  currentRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  menus = session.query(MenuItem).filter_by(restaurant_id = currentRestaurant.id)
  return render_template("menu.html", restaurant = currentRestaurant, items = menus)

  return output


# Task 1: Create route for newMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/new", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    name = request.form['name']
    newMenuItem = MenuItem(restaurant_id = restaurant_id, name = name)
    session.add(newMenuItem)
    session.commit()
    return redirect(url_for("Restaurants", restaurant_id = restaurant_id))
  else:
    return render_template("newmenuitem.html", restaurant_id  = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
  if request.method == 'POST':
    if request.form[name]:
      menuItem.name = request.form[name]
    session.add(menuItem)
    session.commit()
    return redirect(url_for("Restaurants", resturant_id = restaurant_id))
  else:
    return render_template("editmenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, i = menuItem)

    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete")
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

@app.route("/hello")
def HelloWorld():
  return "Hello World"

if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)    