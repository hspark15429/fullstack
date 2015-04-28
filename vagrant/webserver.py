from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import setupDB #  set up SQLALCHEMY, created a session with restaurantMenu attached.

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
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'''
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
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"</form>'''
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
				RnamesHTML = ""
				for name in restaurant_names:
					RnamesHTML += "<li>" + name + "</li>"
				
				output = ""
				output += "<html><body>"
				output += "<ul>{}</ul>".format(RnamesHTML)
				output += "</html></body>"

				self.wfile.write(output)
				print(output)
				return

		except IOError:
			self.send_error(404, "File Not Found {}".format(self.path))

	def do_POST(self):
		try:	
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')

			output = ''
			output += '<html><body>'
			output += '<h2> Okay, how about this: </h2>'
			output += '<h1> {} </h1>'.format(messagecontent[0])
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
			output += '</body></html>'
			self.wfile.write(output)
			print (output)

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
