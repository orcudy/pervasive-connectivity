import matplotlib.pyplot as plt
import numpy as np
import csvutils as csv
import utils
import linalg

#projection onto first two principals components
def renderIrisPCA(eigenvectors, data, species):
        pc1 = eigenvectors[:,0]
        pc2 = eigenvectors[:,1]
        x = np.dot(data.T, pc1)
        y = np.dot(data.T, pc2)
        plt.plot(x[0:50], y[0:50], 'go', label='Setosa')
        plt.plot(x[50:100], y[50:100], 'yo', label='Versicolor')
        plt.plot(x[100:150], y[100:150], 'ro', label='Virginica')
        plt.title('PCA on Iris Data Set')
        plt.ylabel('Second Principal Component')
        plt.xlabel('First Principal Component')
        plt.legend(loc='upper left', numpoints=1)
        plt.show()

def main():
        #get file handle
        path = '/home/orcudy/Desktop/cs170a/data/Iris.csv'
        fd = open(path, 'r')
        lines = list(fd)
        fd.close()

        #retrieve flower data
        featureIDs = csv.generateFeatureIDList(lines, ',')

        #remove whitespace from IDs
        for index in range(len(featureIDs)):
                featureIDs[index] = filter(lambda x: x.isalnum(), featureIDs[index])
  
        #generate feature map and convert to appropriate type
        floatConversionUnit = (featureIDs, lambda x: float(x) if utils.isfloat(x) else -1.0)
        dataMap = csv.convertType( csv.generateDataMap(lines, featureIDs), [floatConversionUnit])
        

        #set parameters for analysis
        species = csv.generateArray(dataMap, ['Species']).T
        basePath =  '/home/orcudy/Desktop/cs170a/logs'
        ID = 'iris'
        data = csv.generateArray(dataMap, featureIDs)
        correlation = linalg.computeCorrelationMatrix(data, featureIDs, True, basePath, ID)
        u, s, vt = linalg.computeSVD(correlation, featureIDs, True, basePath, ID)
        renderIrisPCA(u, data, species)
        
main()
		
