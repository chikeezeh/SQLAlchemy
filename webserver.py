from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
# The following codes will connect to the database
# and query it for data, so that it can be presented on the
# HTML page
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                # creates a link for adding a new restaurant
                output += "<a href='/restaurants/new'> Create A new Restaurant</br></br></a>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href ='#'>Edit</a></br>"
                    output += "<a href ='#'>Delete</a></br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                # form to accept new Restaurant
                output += """ <form method = 'POST' enctype ='multipart/form-data'>
                <h2>Enter A new Restaurant</h2>
                <input name ='newRestaurantName' type ='text' placeholder ='New Restaurant'>
                <input type ='submit' value = 'Create'></form> """
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new restaurant object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # redirect to homepage
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except IOError:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web sever..."
        server.socket.close()


if __name__ == '__main__':
    main()
