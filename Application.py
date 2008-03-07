
import cherrypy
import pickle


# This class contains the methods that correspond to URLs
class CTFServer:

	preferencesArray = {}

	# This method (index) will be called if no other URL is given
	# /ctf-app/
	@cherrypy.expose
	def index(self, *args, **kwargs):
		
		return "<p>Foo Bar!</p><p>%s</p>" % kwargs
	
	# /ctf-app/scoreboard/
	@cherrypy.expose	
	def scoreboard(self, *args, **kwargs):
		f = open("/home/cs206/facebook-ctf/static/scoreboard.html")
		html = f.read()
		f.close()
		return html
		
	# /ctf-app/preferences/
	@cherrypy.expose
	def preferences(self, *args, **kwargs):
		return "<p>Preferences stuff goes here...</p>"
		

	@cherrypy.expose
	def saveprefs(self, *args, **kwargs):
		
		preferenceArraySize = 0

		#creates a string
		keyStrings = "teamName teamColor individualColor numberOfFlags terrain grid"

		#splits the string into several strings and splits by spaces
		keyStrings.split()

		for preference in keyStrings:
			preferencesArray[preferenceArraySize] = kwargs[keyStrings]
			preferenceArraySize += 1

		return str(preferences)

		#prefSize=0
		#a=0
		#y=0
		#foundString = False

		#while y < 7:
		#	if kwargs[a] == "teamName":
		#		preferences[prefSize] = kwargs["teamName"]
		#		foundString = true
		#	elif kwargs[a] == "teamColor":
		#		preferences[prefSize] = kwargs[a]
		#		foundString = true
		#	elif kwargs[a] == "individualColor":
		#		preferences[prefSize] = kwargs[a]
		#		foundString = true
		#	elif kwargs[a] == "numberOfFlags":
		#		preferences[prefSize] = kwargs[a]
		#		foundString = true
		#	elif kwargs[a] == "terrain":
		#		preferences[prefSize] = kwargs[a]
		#		foundString = true
		#	elif kwargs[a] == "grid":
		#		preferences[prefSize] = kwargs[a]
		#		foundString = true
		#	
		#	if foundString == True:
		#		y += 1
		#		z += 1
		#		a += 1
		#		foundString = False
		#

	@cherrypy.expose
	def game(self, *args, **kwargs):
		html = ""
		f = open("/home/cs206/facebook-ctf/static/game_board_copy.html")
		for line in f:
			html += line
			if line.find("tiles get loaded here") != -1:
				map = pickle.load(open("/home/cs206/facebook-ctf/map3.map"))
				for row in map:
					for tile in row:
						html += "<img src=\"http://facebook.justinvoss.com/static/%s\" alt=tile />" % tile
		f.close()
		return html

# This sets the port that Cherrypy will be serving on		
conf = {
	'server.socket_port': 8800,
}
cherrypy.config.update(conf)
	
# This actually starts the server
cherrypy.quickstart( CTFServer() )
