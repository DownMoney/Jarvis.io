import urllib2
import json

def GetCurrentLocation():
	res = urllib2.urlopen('http://ip-api.com/json')
	j = json.loads(res.read())
	return {'Response': {'text': j['city'], 'html': '<h1>'+j['city']+'</h1>'}, 'AdditionalData': {'currentCity': j['city'], 'currentCountry': j['country'], 'isp': j['isp'], 'ip': j['query']}}




def Process(query, params, FB):
	fb = FB.getFactBase()
	if params['action'][0] in fb:
		return {'Response': {'text': fb[params['action'][0]], 'html': ''}, 'AdditionalData': {}}

	return {}

def Trigger(data, FB):
	return ''

def getMethods():
	return {
		'GetCurrentLocation': GetCurrentLocation
	}