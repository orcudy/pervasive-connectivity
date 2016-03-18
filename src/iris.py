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

def svd(array):
    cov = np.cov(array)
    return np.linalg.svd(cov)
    
def main():
    path = '/home/orcudy/Desktop/cs170a/data/Iris-small.csv'
    fd = open(path, 'r')
    rawLines = list(fd)
    fd.close()

    lines = removeWhitespace(rawLines)

    featureIDs = csv.generateFeatureIDList(lines, ',')
    conversionUnit = [(featureIDs, lambda x: float(x))]
    
    rawFeatureMap = csv.generateDataMap(lines, featureIDs)
    featureMap = csv.convertType(rawFeatureMap, conversionUnit)
    featureArray = csv.generateArray(featureMap, featureIDs)

    maskValues = []
    mask = csv.generateDataMask(featureArray, maskValues)
    maskedArray = np.ma.masked_array(featureArray, mask)
    cov = np.ma.cov(maskedArray)
    logpath = '/home/orcudy/Desktop/cs170a/logs/iris_cov.csv'
    csv.writeToCSV(cov, logpath, [' '] + featureIDs, featureIDs)

    corr = np.ma.corrcoef(maskedArray)
    logpath = '/home/orcudy/Desktop/cs170a/logs/iris_corr.csv'
    csv.writeToCSV(corr, logpath, [' '] + featureIDs, featureIDs)

    u, s, vt = np.linalg.svd(cov)
    logpath = '/home/orcudy/Desktop/cs170a/logs/iris_svd.csv'
    csv.writeToCSV(u, logpath, ['eigenvalues'], featureIDs)

main()


