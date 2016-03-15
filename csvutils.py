import numpy as np

#generate a dictionary where keys are question IDs and value is list of answers
#Note: -1 replaced blank entries
def generateResponseMap(path):
        fd = open(path, 'r')
        lines = list(fd)
        fd.close()
        
        questionIDMap =  generateQuestionIDMap(lines)
        questionIDs = map(lambda x: questionIDMap[x], questionIDMap)
        
        #data dynamics
        chars = ['usr']
        floats = ['weight', 'standwt']
        ints = filter(lambda x: x not in chars + floats, questionIDs)

        #conversion dynamics
        def isfloat(string):
	        try:
		        float(string)
		        return True
	        except:
		        return False
        floatConversionUnit = (floats, lambda x: float(x) if isfloat(x) else -1.0)
        intConversionUnit = (ints, lambda x: int(x) if x.isdigit() else -1)
        
        return convertTypes(generateRawResponseMap(lines, questionIDMap), [floatConversionUnit, intConversionUnit])
        
#generate index to question ID lookup table
def generateQuestionIDMap(lines):
        questionIDMap = {}
        questionIDs = lines[0].split(',')

        #cleanup first and last token (other tokens do not need cleaning)
        def removeNonAlnum(string):
                return filter(lambda x: x.isalnum(), string)
        questionIDs[0] =  removeNonAlnum(questionIDs[0])
        questionIDs[-1] =  removeNonAlnum(questionIDs[-1])
        
        for index in xrange(len(questionIDs)):
                questionIDMap[index] = questionIDs[index]
        return questionIDMap

#generate question ID to responses lookup table
def generateRawResponseMap(lines, questionIDMap):
        responseMap = {}
        for line_index in xrange(1, len(lines)):
	        responses = lines[line_index].split(',')
	        for index in xrange(len(responses)):
		        key = questionIDMap[index]
		        response = responses[index]
		        if key not in responseMap:
			        responseMap[key] = [response]
		        else: 
			        responseMap[key].append(response)
        return responseMap

#convert responses to appropriate type
def convertTypes(responseMap, conversionUnits):
        for unit in conversionUnits:
                for key in unit[0]:
                        responseMap[key] = map(unit[1], responseMap[key])
        return responseMap

#create 2D numpy array using data from specified question keys
def generateArray(responseMap, questionIDs):
        xdim = len(questionIDs)
        ydim = len(responseMap[questionIDs[0]])
        mtype = type(responseMap[questionIDs[0]][0])
        newMap = np.empty((xdim, ydim), mtype)
        for index in xrange(len(questionIDs)):
                newMap[index] = responseMap[questionIDs[index]]
        return newMap
        
def main():
        responseMap = generateResponseMap('/home/orcudy/Desktop/cs170a/CSV.csv')
        
        demographic_keys = ['sex',
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
        demographics = generateArray(responseMap, demographic_keys)
        for index in xrange(len(demographic_keys)):
                print(demographic_keys[index])
                print(demographics[index])
                print

        
        

main()
		
