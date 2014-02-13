import nltk
from nltk import parse_cfg
from nltk import parse
from nltk import Tree
import Modules
from FactBase import FactBase
import random

extraction = {"action": ["NN", "VB"], "object": ["NNP", "NNS", "VBN"], "params": ["CD", "JJS"]}
triggerProb = 1.0
factBase = FactBase()

modules = {}

for m in Modules.__all__:
    mod = m.split('.')
    modules[mod[len(mod)-1]] = __import__(m, globals(), locals(), [mod[len(mod)-1]], -1)


def extract(tags):
	vals = {"action": [], "object": [], "params": []}

	for t in tags:
		if t[1] in extraction["action"]:
			vals["action"]+=[t[0]]
		if t[1] in extraction["object"]:
			vals["object"]+=[t[0]]
		if t[1] in extraction["params"]:
			vals["params"]+=[t[0]]

	return vals

def Trigger(data):
	if len(data.items())>0:
		r = random.random()
		if r <= triggerProb:		
			fact = random.choice(data.items())
			for m in modules:
				res = modules[m].Trigger(fact, factBase)
				if res != '':
					return res
		

def AddFacts(data):
	factBase.addFacts(data)
	return Trigger(data)

def process(query, params):
	for action in params['action']:
		if action in modules.keys():
			module = modules[params['action'][0]]
			response = module.Process(query, params, factBase)
			if 'Response' in response:	
				print query
				if 'AdditionalData' in response:
					response['Trigger'] = AddFacts(response['AdditionalData'])
				return response

	return {}



f = open('testFile.txt', 'r')

for line in f:
	text = nltk.word_tokenize(line)
	tagging = nltk.pos_tag(text)
	print tagging
	params = extract(tagging)
	print params
	#res = process(line, params)
	#if res != {}:
	#	print res['Response']['text']
	#	if res['Trigger'] != None:
	#		print res['Trigger']

	print ''
