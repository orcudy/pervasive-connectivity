#float utility
def isfloat(string):
	try:
		float(string)
		return True
	except:
		return False
