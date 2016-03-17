import numpy as np
import csvutils
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
    
def convertToCSV(dataArray, path, topCellIDs = [], leftCellIDs = []):
    fd = open(path, 'w')

    #write top cell labels
    for ID in topCellIDs:
        fd.write(ID + ',')
    fd.write('\n')

    
    xdim, ydim = dataArray.shape
    for x in range(xdim):
        if x < len(leftCellIDs):
            fd.write(leftCellIDs[x] + ',')
        for y in range(ydim):
            fd.write("%.5f" % dataArray[x][y] + ',')
        fd.write('\n')
    fd.close()    
    
    

def main():
    path = '/home/orcudy/Desktop/cs170a/data/Iris-small.csv'
    fd = open(path, 'r')
    rawLines = list(fd)
    fd.close()

    lines = removeWhitespace(rawLines)

    featureIDs = csvutils.generateFeatureIDList(lines, ',')
    conversionUnit = [(featureIDs, lambda x: float(x))]
    
    rawFeatureMap = csvutils.generateDataMap(lines, featureIDs)
    featureMap = csvutils.convertType(rawFeatureMap, conversionUnit)
    featureArray = csvutils.generateArray(featureMap, featureIDs)

    maskValues = []
    mask = csvutils.generateDataMask(featureArray, maskValues)
    maskedArray = np.ma.masked_array(featureArray, mask)
    cov = np.ma.cov(maskedArray)
    logpath = '/home/orcudy/Desktop/cs170a/logs/iris_cov.csv'
    convertToCSV(cov, logpath, [' '] + featureIDs, featureIDs)

    corr = np.ma.corrcoef(maskedArray)
    logpath = '/home/orcudy/Desktop/cs170a/logs/iris_corr.csv'
    convertToCSV(corr, logpath, [' '] + featureIDs, featureIDs)

    u, s, vt = np.linalg.svd(cov)
    logpath = '/home/orcudy/Desktop/cs170a/logs/iris_svd.csv'
    convertToCSV(u, logpath, ['eigenvalues'], featureIDs)

    
main()


