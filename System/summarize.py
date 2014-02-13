 # -*- coding: latin-1 -*-

from __future__ import division
import nltk
import operator
import urllib2
import math
import MLStripper
import re
from readability.readability import Document
import lxml.html


class Summarize(object):
	"""docstring for summarize"""
	def __init__(self):		
		self.freq = {}
		self.sentences = []
		self.data = ''

	def checkSentence(self,s,x):
		if len(s)>50:
			return False
		for word in self.freq[:x]:
			if not (word[0] in s):
				return False

		return True

	def summarize(self,url):
		self.data = urllib2.urlopen(url).read()
		self.data = Document(self.data).summary()
		
		self.data = MLStripper.strip_tags(self.data).replace('\n', ' ').replace(',', ' ').replace('\t', ' ').replace("'", "").replace('"', ' ').replace('(',' ').replace(')', ' ').replace(':', ' ').replace(']', ' ').replace('[', ' ').replace(';', ' ')
		self.data = self.data.lower()
		temp = self.data.split('.')
		

		text = re.findall(r'([a-z]+|\d+)+', self.data)

		for t in temp:
			self.sentences += [' '.join(re.findall(r'([a-z]+|\d+)+', t))]	

		self.freq = {}

		for word in text:
			if word in self.freq:
				self.freq[word] += 1
			else:
				self.freq[word] = 1

		self.freq = sorted(self.freq.iteritems(), key=operator.itemgetter(1))
		self.freq.reverse()
		t = lxml.html.parse(url)
		title = t.find(".//title").text
		return {'title': title, 'summary': self.evaluate(0.01)}

	def evaluate(self,d):
		output = ''

		num = len(self.freq)
		num = int(math.floor(num*d))

		for sentence in self.sentences:
			s = re.findall(r'[a-z]+', sentence)
			if self.checkSentence(s, num) == True:
				output += sentence[0].upper()+sentence[1:]+'. '	

		compression = 1-(len(output)/len(self.data))

		if compression >= 0.80:
			return self.evaluate(d-.001)

		if compression <= 0.60:
			return self.evaluate(d+.001)

		return output


#s = Summarize()

#print s.summarize('http://www.bbc.co.uk/news/uk-25996176')