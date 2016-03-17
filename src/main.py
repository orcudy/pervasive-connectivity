
#conversion dynamics
def isfloat(string):
	try:
		float(string)
		return True
	except:
		return False
        
def main():
        #data dynamics
        chars = ['usr']
        floats = ['weight', 'standwt']
        ints = filter(lambda x: x not in chars + floats, questionIDs)
        floatConversionUnit = (floats, lambda x: float(x) if isfloat(x) else -1.0)
        intConversionUnit = (ints, lambda x: int(x) if x.isdigit() else -1)
        
        path = '/home/orcudy/Desktop/cs170a/CSV.csv'
        fd = open(path, 'r')
        lines = list(fd)
        fd.close()
        
        questionIDMap =  generateQuestionIDMap(lines)
        questionIDs = map(lambda x: questionIDMap[x], questionIDMap)
        rawResponseMap = generateResponseMap(lines, questionIDMap)
        responseMap = convertType(rawResponseMap, [floatConversionUnit, intConversionUnit])
        demographicKeys = ['sex',
                            'marital',
                            'par',
                            'ql1',
                            'smart1',
                            'age',
                            'hh1',
                            'live2',
                            'educ2',
                            'emplnw',
                            'hisp',
                            'birth_hisp',
                            'race',
                            'inc',
                            'zipcode']
        
        demographics = generateArray(responseMap, demographicKeys)
        
main()
		
