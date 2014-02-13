import urllib2
import simplejson

endpoint = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=')


def Search(query):
	query = query.replace(' ', '+')
	request = urllib2.Request(endpoint+query, None, {'Referer': 'Jarvis'})
	response = urllib2.urlopen(request)
	results = simplejson.load(response)
	return results


print Search('Bill Gates')