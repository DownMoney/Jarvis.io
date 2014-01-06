import nltk
from nltk import parse_cfg
from nltk import parse
from nltk import Tree
import Modules
from FactBase import FactBase
import random

extraction = {"action": ["NN", "VB"], "object": ["NNP", "NNS", "VBN"], "params": ["CD"]}
triggerProb = 0.4
factBase = FactBase()

modules = []

for m in Modules.__all__:
    mod = m.split('.')
    modules += [__import__(m, globals(), locals(), [mod[len(mod)-1]], -1)]


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
	r = random.random()
	if r <= triggerProb:		
		fact = random.choice(data.items())
		for m in modules:
			res = m.Trigger(fact, factBase)
			if res != '':
				print res
		

def AddFacts(data):
	factBase.addFacts(data)
	Trigger(data)

def process(query, params):
	for module in modules:
		response = module.Process(query, params)
		if response != '':	
			print query
			print response['Response']['text']
			AddFacts(response['AdditionalData'])
			

	return ''



f = open('testFile.txt', 'r')

for line in f:
	text = nltk.word_tokenize(line)
	tagging = nltk.pos_tag(text)
	params = extract(tagging)
	res = process(line, params)
	if res != '':
		print res
