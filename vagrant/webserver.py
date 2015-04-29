from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import setupDB #  set up SQLALCHEMY, created a session with restaurantMenu attached.
import re


class webServerHandler(BaseHTTPRequestHandler):
	#  make calling from setupDB module simpler
	session = setupDB.session
	Restaurant = setupDB.Restaurant
	MenuItem = setupDB.MenuItem

	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body><h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'''
				output += "</body></html>"

				self.wfile.write(output)
				print(output)
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body><h1>&#161 Hola !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'''
				output += "</body></html>"

				self.wfile.write(output)
				print(output)
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurants = self.session.query(self.Restaurant).all()
				restaurant_names = [restaurant.name for restaurant in restaurants]
				restaurant_ids = [restaurant.id for restaurant in restaurants]
				RnamesHTML = ""
				for name, restaurant_id in zip(restaurant_names, restaurant_ids):
					RnamesHTML += "<li>" + name + "</li>" + "<a href='restaurants/{}/edit'>Edit</a>".format(restaurant_id)\
								  + "</br>" + "<a href='#'>Delete</a>"
				
				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
				output += "<ul>{}</ul>".format(RnamesHTML)
				output += "</html></body>"

				self.wfile.write(output)
				# print(output)
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += '''<form method='POST' enctype='multipart/form-data'><h2>Make a New Restaurant</h2><input name="newRestaurant" type="text"><input type="submit" value="Submit"></form>'''
				output += "</body></html>"

				self.wfile.write(output)
				return

			if re.match(".*/restaurants/[0-9]+/edit", self.path):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurant_id = int(re.match(".*/restaurants/([0-9]+)/edit", self.path).group(1))
				thisRestaurant = self.session.query(self.Restaurant).filter_by(id=restaurant_id).one()

				output = ""
				output += "<html><body>"
				output += "<h1>"+thisRestaurant.name+"</h1>"
				output += '''<form method='POST' enctype='multipart/form-data'><input name="newName" type="text"><input type="submit" value="Rename"></form>'''
				output += "</body></html>"

				self.wfile.write(output)
				return


		except IOError:
			self.send_error(404, "File Not Found {}".format(self.path))

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):

				ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurant')

				newRestaurant = self.Restaurant(name = messagecontent[0])

				self.session.add(newRestaurant)
				self.session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('location', '/restaurants')
				self.end_headers()

				return

			if re.match(".*/restaurants/[0-9]+/edit", self.path):

				ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newName')
				
				restaurant_id = int(re.match(".*/restaurants/([0-9]+)/edit", self.path).group(1))
				thisRestaurant = self.session.query(self.Restaurant).filter_by(id=restaurant_id).one()
				thisRestaurant.name = messagecontent[0]
				self.session.add(thisRestaurant)
				self.session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('location', '/restaurants')
				self.end_headers()

		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print('Web server running on port {}'.format(port))
		server.serve_forever()
	except KeyboardInterrupt:
		print("^C entered, stopping web server...")
		server.socket.close()

if __name__ == '__main__':
	main()
