import nltk
from nltk import parse_cfg
from nltk import parse
from nltk import Tree
import Modules
from FactBase import FactBase
import random
import re
from speak import Speak


extraction = {"action": ["NN", "VB"], "object": ["NNP", "NNS", "VBN", "VBP"], "params": ["CD"]}

triggerProb = 1.0
factBase = FactBase()

modules = {}

for m in Modules.__all__:
    mod = m.split('.')
    name = mod[len(mod)-1]
    modules[name] = {}
    modules[name]['module'] = __import__(m, globals(), locals(), [mod[len(mod)-1]], -1)
    methods = []
    for x in dir(modules[name]['module']):
    	if not '__' in x:
    		methods += [x]
    	else:
    		break


    modules[name]['methods'] = methods


def extract(tags):
	vals = {"action": [], "object": [], "params": []}

	for t in tags:
		if t[1] in extraction["action"]:
			vals["action"]+=[(t[0], t[1])]
		if t[1] in extraction["object"]:
			vals["object"]+=[(t[0], t[1])]
		if t[1] in extraction["params"]:
			vals["params"]+=[(t[0], t[1])]

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

	for module in modules:
		print dir(module)
		response = module.Process(query, params, factBase)
		if 'Response' in response:	
			print query
			if 'AdditionalData' in response:
				response['Trigger'] = AddFacts(response['AdditionalData'])
			return response

	return {}

def convertToExpression(params):
	expr = ''
	expr = params['action'][0][0] +'('
	for a in params['action'][1:]:
		expr+='"'+a[0]+'/'+a[1]+'",'

	for o in params['object']:
		expr+='"'+o[0]+'/'+o[1]+'",'

	for p in params['params']:
		expr+='"'+p[0]+'/'+p[1]+'",'

	expr = expr[:len(expr)-1] + ')'

	return expr

def evaluate(expr):
	
	m = re.search(r'(\w+)\((.+)\)', expr)
	methodName = m.group(1).lower()
	methodName = methodName[0].upper()+methodName[1:]
	args = m.group(2).split(',')

	for i in xrange(len(args)):
		if '"' in args[i]:
			args[i] = args[i][1:-1]
			s = args[i].split('/')
			args[i] = (s[0], s[1])
		else:
			args[i] = evaluate(args[i])
	
	method = None
	moduleRef = None
	for module in modules:
		
		if methodName in modules[module]['methods']:
			moduleRef = modules[module]['module']
			method = getattr(modules[module]['module'], methodName)


	if not method == None:		
		print moduleRef.HowSolve(methodName, args)
		return {'Result':method(args), 'Module': moduleRef}

	return {}

f = open('testFile.txt', 'r')

for line in f:
	print '>'+line.replace('\n','')
	text = nltk.word_tokenize(line)
	tagging = nltk.pos_tag(text)
	print tagging
	params = extract(tagging)
	expr = convertToExpression(params)
	print expr
	res = evaluate(expr)
	if res != {}:
		#Speak(res['Result']['Response']['text'])
		print '<'+res['Result']['Response']['text']
		data = res['Result']['AdditionalData']
		factBase.addFacts(data)
		r = random.random()
		if data != {} and r <= triggerProb:				
			fact = random.choice(data.items())
			trig = res['Module'].Trigger(fact, factBase)
			if trig != '':
				print '<'+trig

	print '\n'
	#print params

	#res = process(line, params)
	#if res != {}:
	#	print res['Response']['text']
	#	if res['Trigger'] != None:
	#		print res['Trigger']

	#print ''
