import urllib2
import json

def GetCurrentLocation():
	res = urllib2.urlopen('http://ip-api.com/json')
	j = json.loads(res.read())
	return {'Response': {'text': j['city'], 'html': '<h1>'+j['city']+'</h1>'}, 'AdditionalData': {'currentCity': j['city'], 'currentCountry': j['country'], 'isp': j['isp'], 'ip': j['query']}}