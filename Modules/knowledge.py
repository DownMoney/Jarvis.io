import sys
import re
import urllib2
from KB import duckduckgo
from KB import bing

sys.path.append("../")

from System.summarize import Summarize

numScan = 5

def Search(query):
	#return duckduckgo.Search(query)
	links = bing.Search(query)
	text = []
	for i in xrange(0,numScan):
		s = Summarize()
		try:
			text+=[s.summarize(links[i])['summary']]
		except Exception, e:
			print e
		

	return (text)



def RegexSearch(regex, query):
	result = duckduckgo.Search(query)	
	for r in result['Results']:
		url = r['FirstURL']
		html = urllib2.urlopen(url).read()
		m = re.search(regex, html)
		return m



t = Search('game of thrones season 4')

for a in t:
	print a
	print '\n------------------------------------------------------------\n'