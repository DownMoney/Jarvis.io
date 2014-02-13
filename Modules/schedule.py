import knowledge

def HowSolve(method, params):
	pass

def Trigger(data, FB):
	return ''

def Time(params):
	thing = ''
	for p in params:
		if p[1] == 'NN':
			thing = p[0]


	response = knowledge.RegexSearch(r'(\d?\d:\d\d?)\s?(AM|PM)?',thing)
	if response !=None:
		return {'Response': {'html': '', 'text': response.group(0)}, 'AdditionalData': {thing+'_time': response.group(0)}}
	else:
		return {'Response': {'html': '', 'text': 'Don\'t know'}, 'AdditionalData': {}}