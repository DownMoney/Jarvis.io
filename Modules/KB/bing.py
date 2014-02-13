import urllib2
import simplejson
import base64

key = 'Bh7IvSdL5AOJYLVWJ9Gg8xTpaKCxOxBvY5loZbrqjoU'
endpoint = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?$format=JSON&Sources=%27web%27&Query="

def Search(query):
	request = urllib2.Request(endpoint+"'"+query.replace(' ', '+')+"'")
	base64string = base64.encodestring('%s:%s' % (key, key)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	result = simplejson.load(urllib2.urlopen(request))
	links = []
	for r in result['d']['results'][0]['Web']:
		links += [r['Url']]

	return links

Search('bill gates')