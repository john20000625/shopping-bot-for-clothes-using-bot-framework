def typ_cal(text1):
	if '连衣裙' in str(text1):
		return {'typ-upper':0,'typ-dress':10}
	else:
		return {'typ-upper':10,'typ-dress':0} 
