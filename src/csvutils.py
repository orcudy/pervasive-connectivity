import numpy as np
        
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
def generateResponseMap(lines, questionIDMap):
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

def countResponses(responseList):
        countMap = {}
        for entry in responseList:
                if entry not in countMap:
                        countMap[entry] = (entry, 1)
                else:
                        countMap[entry] = (countMap[entry][0], countMap[entry][1] + 1)
                return map(lambda x: countMap[x], countMap.keys())
