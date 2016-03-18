import matplotlib.pyplot as plt
import numpy as np
import csvutils as csv
import utils
import keys

#projection onto first two principals components
def renderPCA(eigenvectors, data, position):
        pc1 = eigenvectors[:,0]
        pc2 = eigenvectors[:,1]
        x = np.dot(data.T, pc1)
        y = np.dot(data.T, pc2)
        for index in range(len(x)):
                sentiment = position[index]
                if sentiment == 1:
                        color = "go"
                elif sentiment == 2:
                        color = "yo"
                elif sentiment == 3:
                        color = "mo"
                elif sentiment == 4:
                        color = "ro"
                else:
                        color = "ko"
                plt.plot(x[index], y[index], color)
        plt.show()

def computeCorrelationMatrix(data, keys=[], log=False, path='', keyname=''):
        correlation = np.ma.corrcoef(data)
        print 'correlation'
        print correlation
        if log and path and keyname:
                corr_path = path + '/' + keyname + '_corr.csv'
                csv.writeToCSV(correlation, corr_path, [''] + keys, keys)
        return correlation
                        
def computeSVD(data, keys=[], log=False, path='', keyname=''):        
        u, s, vt = np.linalg.svd(data)
        print 'u of svd'
        print u
        if log and path and keyname:
                svd_path = path + '/' + keyname + '_svd.csv'
                csv.writeToCSV(u, svd_path, [], keys)
        return u, s, vt
        
def generateMaskedArray(dataMap, keys, maskValues):
        data = csv.generateArray(dataMap, keys)
        mask = csv.generateDataMask(data, maskValues)
        return np.ma.masked_array(data, mask)
        
def main():
        #retrieve raw data
        path = '/home/orcudy/Desktop/cs170a/data/CSV.csv'
        fd = open(path, 'r')
        lines = list(fd)
        fd.close()

        #cleanup first and last question IDs (others are already clean)
        lines[0] = lines[0].split(',')
        for index in [0,-1]:
                lines[0][index] = filter(lambda x: x.isalnum(), lines[0][index])
        lines[0] = ','.join(lines[0])

        #retrieve question IDs
        questionIDs =  csv.generateFeatureIDList(lines, ',')

        #data dynamics
        chars = ['usr']
        floats = ['weight', 'standwt']
        ints = filter(lambda x: x not in chars + floats, questionIDs)
        
        #convert feature map to appropriate type
        floatConversionUnit = (floats, lambda x: float(x) if utils.isfloat(x) else -1.0)
        intConversionUnit = (ints, lambda x: int(x) if x.isdigit() else -1)
        responseMap = csv.convertType( csv.generateDataMap(lines, questionIDs), [floatConversionUnit, intConversionUnit])

        #mask "Don't know" and "Refused" responses
        maskValues = [-1, 8, 9, 98, 99, 998, 999, 9998, 9999, 99999]
        position = csv.generateArray(responseMap, keys.position).T
        basePath = '/home/orcudy/Desktop/cs170a/logs'

        datakeys = [keys.phone, keys.control, keys.internet, keys.social, keys.exclusion]
        IDs = ['phone', 'quality', 'control', 'internet', 'social', 'exclusion']
        for index in range(len(datakeys)):
                key = datakeys[index]

                print 'key'
                print key
                ID =  IDs[index]
                print 'ID'
                print ID
                data = csv.generateArray(responseMap, key)
                print 'data'
                print data
                correlation = computeCorrelationMatrix(data, key, True, basePath, ID)
                print 'correlation'
                print correlation
                u, s, vt = computeSVD(correlation, True, basePath, ID)
                renderPCA(u, data, position)

        
        '''
        demographic = generateMaskedArray(responseMap, keys.demographic, maskValues)
        
        #computer correlation matrix and write to csv file
        correlation = np.ma.corrcoef(demographic)
        path = '/home/orcudy/Desktop/cs170a/logs/demographics_corr.csv'
        csv.writeToCSV(correlation, path, [''] + keys.demographic, keys.demographic)

        #find principle components
        u, s, vt = np.linalg.svd(correlation)
        path = '/home/orcudy/Desktop/cs170a/logs/demographics_svd.csv'
        csv.writeToCSV(u, path, [], keys.demographic)
        '''
        
        '''
        position = csv.generateArray(responseMap, keys.position).T
        #projection onto first two principals components
        pc1 = u[:,0]
        pc2 = u[:,1]
        x = np.dot(demographic.T, pc1)
        print('len of x')
        print len(x)
        y = np.dot(demographic.T, pc2)
        for pos in [1,2,3,4]:
                for index in range(len(x)):
                        sentiment = position[index]
                        if sentiment == 1 and pos == 1:
                                color = "go"
                                plt.plot(x[index], y[index], color)
                        elif sentiment == 2 and pos == 2:
                                color = "yo"
                                plt.plot(x[index], y[index], color)
                        elif sentiment == 3 and pos == 3:
                                color = "mo"
                                plt.plot(x[index], y[index], color)
                        elif sentiment == 4 and pos == 4:
                                color = "ro"
                                plt.plot(x[index], y[index], color)
                        else:
                                color = "ko"

                plt.show()
        '''
        
main()
		
