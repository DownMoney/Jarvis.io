import sys
import re
import urllib2
from KB import duckduckgo
sys.path.append("../")

import Jarvis.System.summarize



def Search(query):
	return duckduckgo.Search(query)

def RegexSearch(regex, query):
	result = duckduckgo.Search(query)	
	for r in result['Results']:
		url = r['FirstURL']
		html = urllib2.urlopen(url).read()
		m = re.search(regex, html)
		return m

