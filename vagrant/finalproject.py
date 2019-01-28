from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route("/")
@app.route("/restaurants/")
def  showRestaurants():
  # return "This page will show all my restaurants"
  return render_template("restaurants.html", restaurants = restaurants)

@app.route("/restaurant/new")
def  newRestaurant():
  # return "This page will be for making a new restaurant"
  return render_template("newRestaurant.html")

@app.route("/restaurant/<int:restaurant_id>/edit")
def  editRestaurant():
  # return "Edit a Restaurant"
  return render_template("editMenuItem.html", restaurant)

@app.route("/restaurant/<int:restaurant_id>/delete")
def  deleteRestaurant(restaurant_id):
  # return "Delete all Restaurant"
  return render_template("deleteRestaurant.html", restaurant = restaurant)

@app.route("/restaurant/<int:restaurant_id>")
@app.route("/restaurant/<int:restaurant_id>/menu")
def  showMenu():
  return "SHow all Restaurant"

@app.route("/restaurant/<int:restaurant_id>/menu/new")
def newMenuItem():
  return "Create a new menu item"

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit")
def editMenuItem():
  return "Edit a menu item"

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete")
def deleteMenuItem():
  return "Delete a menu item"


if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)    