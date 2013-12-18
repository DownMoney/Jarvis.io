def Process(query, params):
	
	return ''

def Trigger(data, FB):
	if data[0] == 'country':
		fb = FB.getFactBase()

		if 'currentCountry' in fb and fb['currentCountry'] != data[1]:
			return 'Are you planning to visit '+data[1]+'? I heard it is very nice!'

	if data[0] == 'city':
		fb = FB.getFactBase()

		if 'currentCity' in fb and fb['currentCity'] != data[1]:
			return 'Are you planning to visit '+data[1]+'? I heard it is very nice!'

	return ''