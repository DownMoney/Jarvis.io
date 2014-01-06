import urllib2
import json
from lxml import etree
import utilities

endpoint = "http://weather.yahooapis.com/forecastrss?format=json&u=c"
acceptedStates = {"action": ["temperature", "weather"], "object": []}
appID = 'cJJ4nPPV34FnTF9Ro2q5_8NdDQ7v3QSIHrJiLOkOq0J1NYK_UHE._6zjjOvcI.QN3rUjC54jH.kgguba8SX.sbp6Qc6eMjE-'


def getWOEID(place):
	url = "http://where.yahooapis.com/v1/places.q('"+place+"')?format=json&appid="+appID
	res = urllib2.urlopen(url)

	return str(json.loads(res.read())['places']['place'][0]['woeid'])


def getWeather(place):
	url = endpoint+"&w="+getWOEID(place)
	res = urllib2.urlopen(url)	
	return etree.fromstring(res.read().replace('yweather:', ''))

def createResponse(xml):
	j = {'Response': {'html': '', 'text': ''}, 'AdditionalData': {'city': '', 'region': '', 'country': '', 'temp': ''}}

	j['Response']['html'] = xml.xpath('//description/text()')

	j['Response']['text'] = "It's " + str(xml.xpath('//condition/@temp')[0]) + " degrees in " + str(xml.xpath('//location/@city')[0])+ "."
	j['AdditionalData']['temp'] = str(xml.xpath('//condition/@temp')[0])
	
	j['AdditionalData']['city'] = str(xml.xpath('//location/@city')[0])
	j['AdditionalData']['region'] = str(xml.xpath('//location/@region')[0])
	j['AdditionalData']['country'] = str(xml.xpath('//location/@country')[0])
	

	return j

def Process(query, params, FB):
	for a in params["action"]:
		if a in acceptedStates["action"]:
			if len(params['object']) == 0:
				params['object'] += [utilities.GetCurrentLocation()['Response']['text']]
			w = getWeather(params['object'][0])
			return createResponse(w)


	return ''

def Trigger(data, FB):
	if data[0] == 'temp':
		if int(data[1]) > 15:
			return 'How are you enjoying this nice weather?'
		else:
			return "Bit chilly isn't? You should wrap up today!"

	return ''
