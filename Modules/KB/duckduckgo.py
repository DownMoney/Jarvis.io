import urllib2
import simplejson

endpoint = 'http://api.duckduckgo.com/?format=json&pretty=1&q='

def Search(topic):
	response = urllib2.urlopen(endpoint+topic)
	results = simplejson.load(response)
	return results