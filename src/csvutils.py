import numpy as np

#input: comma separated csv data and optional delimiting character
#output: list of features
def generateFeatureIDList(lines, delim=' '):
        return lines[0].split(delim)        

#generate index to question ID lookup table
def generateFeatureIDMap(lines, featureIDs):
        featureIDMap = {}
        for index in xrange(len(featureIDs)):
                featureIDMap[index] = featureIDs[index]
        return featureIDMap

#generate question ID to responses lookup table
def generateDataMap(lines, featureIDs):
        featureIDMap = generateFeatureIDMap(lines, featureIDs)
        dataMap = {}
        for line_index in xrange(1, len(lines)):
	        responses = lines[line_index].split(',')
	        for index in xrange(len(responses)):
		        key = featureIDMap[index]
		        response = responses[index]
		        if key not in dataMap:
			        dataMap[key] = [response]
		        else: 
			        dataMap[key].append(response)
        return dataMap

#convert responses to appropriate type
def convertType(dataMap, conversionUnits):
        for unit in conversionUnits:
                for key in unit[0]:
                        dataMap[key] = map(unit[1], dataMap[key])
        return dataMap

#create 2D numpy array using data from specified question keys
def generateArray(dataMap, featureIDs):
        xdim = len(featureIDs)
        ydim = len(dataMap[featureIDs[0]])
        mtype = type(dataMap[featureIDs[0]][0])
        newMap = np.empty((xdim, ydim), mtype)
        for index in xrange(len(featureIDs)):
                newMap[index] = dataMap[featureIDs[index]]
        return newMap

def countResponses(responseList):
        countMap = {}
        for entry in responseList:
                if entry not in countMap:
                        countMap[entry] = (entry, 1)
                else:
                        countMap[entry] = (countMap[entry][0], countMap[entry][1] + 1)
                return map(lambda x: countMap[x], countMap.keys())
