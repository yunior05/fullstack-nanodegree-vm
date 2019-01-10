from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Create Session to Database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class handlerserver(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("/restaurants"):
        self.send_response(200)
        self.send_header("Conten-type", "text/html")
        self.end_headers()

        output = "<html><body>"
        output+= "<h2><a href='restaurants/new'>Make new restaurant</a></h2>"
        restaurants = session.query(Restaurant).all()
        for restaurant in restaurants:
          output+= "<div >%s<div>" % restaurant.name
          output+="<a  href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id
          output+="<a  href='/restaurants/%s/delete'>Delete</a><br>" % restaurant.id
        output += "</body></html>"

        self.wfile.write(output)
        return
      elif self.path.endswith("/restaurants/new"):
        self.send_response(200)
        self.send_header("Conten-type", "text/html")
        self.end_headers()
        
        output = "<html><body>"
        output += "<h2>Create new Restaurant</h2>"
        output += "<br><form method='POST' enctype='multipart/form-data' action='/restaurants/new''>"
        output += "<input type='text' name='restaurantName' placeholder='Insert name of restaurant'> "
        output += "<input type='submit' name='Send' value='Send'>"
        output += "</form>"

        self.wfile.write(output)

      elif self.path.endswith("/edit"):
        self.send_response(200)
        self.send_header("Conten-type", "text/html")
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h2>Rename Restaurant</h2>"
        output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
        output += "<input type='text' name='restaurantName' placeholder='Enter restaurant name...'>"
        output += "<input type='submit' name='send' value='send'>"
        output += "</form>"
        self.wfile.write(output)
        return

      elif self.path.endswith("/hello"):
        self.send_response(200)
        self.send_header("Conten-type", "text/html")
        self.end_headers()

        output = "<html><body>Hello!"
        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        output += "</body></html>"
        self.wfile.write(output)
        return
        
      elif self.path.endswith("/hola"):
        self.send_response(200)
        self.send_header("Conten-type", "text/html")
        self.end_headers()

        output = "<html><body>Hola! <a href='/hello' >Back to Hello</a>"
        output += "</body></html>"
        self.wfile.write(output)
        return
      
      elif self.path.endswith("/delete"):
        self.send_response(200)
        self.send_header("Conten-type", "text/html")
        self.end_headers()
        select_restaurant = session.query(Restaurant).filter_by(id = self.path.split("/")[2] ).one()
        output = ""
        output += "<html><body>"
        output += "<h2> Are you sure you want to delte %s Restaurant?</h2>" % select_restaurant.name
        output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
        output += "<input type='submit' name='Delete' value='Delete'>"
        output += "</form>"
        self.wfile.write(output)
        return

    except IOError:
      self.send_error(404, "File not found")
  
  def do_POST(self):
    try:
      if self.path.endswith("/restaurants/new"):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == "multipart/form-data":
          fields = cgi.parse_multipart(self.rfile, pdict) 
          message_content = fields.get("restaurantName")

        newRestaurant = Restaurant(name=message_content[0])
        session.add(newRestaurant)
        session.commit()
        self.send_response(301)
        self.send_header("Conten-type",   "text/html")
        self.send_header('Location', '/restaurants')
        self.end_headers()

        return 

      # output = ""
      # output += "<html><body>"
      # output += "<h1>Ok, how about this:</h1>"
      # output += "<h2>%s</h2>" % message_content[0]
      # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
      # output += "</html></body>"
      
      # self.wfile.write(output)
      
      elif self.path.endswith("/edit"):

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == "multipart/form-data":
          fields = cgi.parse_multipart(self.rfile, pdict) 
          message_content = fields.get("restaurantName")

        id_restaurant = self.path.split("/")[2]
        select_restaurant = session.query(Restaurant).filter_by(id=id_restaurant).first()
        select_restaurant.name = message_content[0]
        session.commit()

        self.send_response(301)
        self.send_header("Conten-type",   "text/html")
        self.send_header('Location', '/restaurants')
        self.end_headers()
      elif self.path.endswith("/delete"):
        id_restaurant = self.path.split("/")[2]
        select_restaurant = session.query(Restaurant).filter_by(id=id_restaurant).first()
        session.delete(select_restaurant)


        self.send_response(301)
        self.send_header("Conten-type",   "text/html")
        self.send_header('Location', '/restaurants')
        self.end_headers()


    except:
      pass



def main():
  try:
    port = 8080
    server = HTTPServer(('', port), handlerserver)
    print("Server on in dir %s" % port)
    server.serve_forever()

  except KeyboardInterrupt:
    print("Ctrl+C interrupt")
    server.socket.close()

if __name__ == "__main__":
  main()