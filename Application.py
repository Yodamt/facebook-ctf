
import cherrypy
import pickle


# This class contains the methods that correspond to URLs
class CTFServer:

	preferencesArray = []

	# This method (index) will be called if no other URL is given
	# /ctf-app/
	@cherrypy.expose
	def index(self, *args, **kwargs):
		
		return "<p>Foo Bar!</p>"

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
		f = open("/home/cs206/facebook-ctf/static/preferences.html")
		html = f.read()
		f.close()
		uid = kwargs['fb_sig_user']
		try:
			prefs = pickle.load(open("/home/cs206/facebook-ctf/userprefs/%s" % uid))
		except IOError:
			# user hasn't saved preferences before, use default
			prefs = {'teamName':'The Leopards','teamColor':'0'}
			prefs['individualColor'] = prefs['grid'] = '0'
			prefs['numberOfFlags'] = prefs['terrain'] = '0'
		# set the default value for the forms
		html = html.replace('userTeamName', prefs['teamName'])
		last = 0
		for pref in ['teamColor','individualColor','numberOfFlags','terrain','grid']:
			s = prefs[pref]
			start = html.find(pref, last)
			end = html.find("</select>", start)
			section = html[start:end]
			section = section.replace('value="%s"' % s, 'value="%s" selected' % s)
			html = html[:start] + section + html[end:]
			last = end
		return html
		
	@cherrypy.expose
	def saveprefs(self, *args, **kwargs):
		#preferenceArraySize = 0

		#creates a string
		#keyStrings = "teamName teamColor individualColor numberOfFlags terrain grid"

		#splits the string into several strings and splits by spaces
		#keyStrings.split()

		#for preference in keyStrings:
		#	self.preferencesArray[preferenceArraySize] = kwargs[preference]
		#	preferenceArraySize += 1

		#return str(preferences)
		userprefs = {}
		uid = kwargs['fb_sig_user']
		userprefs['teamName'] = kwargs['teamName']
		userprefs['teamColor'] = kwargs['teamColor']
		userprefs['individualColor'] = kwargs['individualColor']
		userprefs['numberOfFlags'] = kwargs['numberOfFlags']
		userprefs['terrain'] = kwargs['terrain']
		userprefs['grid'] = kwargs['grid']
		pickle.dump(userprefs, open("/home/cs206/facebook-ctf/userprefs/%s" % uid, 'w'))
		return "Preferences saved."

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
