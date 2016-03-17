import numpy as np
import csvutils as csv
import matplotlib.pyplot as plt

def removeWhitespace(lines):
    newLines = []
    for line in lines:
        newLine = ""
        for char in line:
            if char != '\n' and char != '\t':
                newLine += char
        if newLine:
            newLines.append(newLine)
    return newLines
            

path = '/home/orcudy/Desktop/cs170a/Iris.csv'
fd = open(path, 'r')
rawLines = list(fd)
fd.close()

lines = removeWhitespace(rawLines)

featureIDMap = csv.generateQuestionIDMap(lines)
rawFeatureMap = csv.generateResponseMap(lines, featureIDMap)
featureNames = ['SepalLength', 'Sepal.Width', 'Petal.Length', 'Petal.Width', 'Species']
conversionUnit = [(featureNames, lambda x: float(x))]
featureMap = csv.convertTypes(rawFeatureMap, conversionUnit)
featureArray = csv.generateArray(featureMap, featureNames).T
print featureArray

#corr = np.corrcoef(featureArray)
cov = np.cov(featureArray)
u, s, vT = np.linalg.svd(cov)
print s
print u
'''
pc1 = u[:,0]
pc2 = u[:,1]
x = np.dot(featureArray.T[0:50], pc1)
y = np.dot(featureArray.T[0:50], pc2) 
plt.plot(x,y, 'r+')

x = np.dot(featureArray.T[50:100], pc1)
y = np.dot(featureArray.T[50:100], pc2) 
plt.plot(x,y, 'g+')

x = np.dot(featureArray.T[100:150], pc1)
y = np.dot(featureArray.T[100:150], pc2) 
plt.plot(x,y, 'b+')
plt.show()
'''
