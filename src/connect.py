import matplotlib.pyplot as plt
import numpy as np
import csvutils as csv
import utils
import keys
import linalg

#projection onto first two principals components
def renderPCA(eigenvectors, data, sentiments, title=''):
        def subplot(hifavor, favor, opposed, hiopposed):
                def setAxis(axis, data, title, color):
                        axis.set_title(title)
                        axis.plot(data[0], data[1], color)
                fig, axis = plt.subplots(2, 2)
                setAxis(axis[0][0], hifavor, 'Highly In Favor', 'go')
                setAxis(axis[0][1], favor, 'In Favor', 'yo')
                setAxis(axis[1][0], opposed, 'Opposed', 'ro')
                setAxis(axis[1][1], hiopposed, 'Highly Opposed', 'ko')
                plt.show()
        def fullplot(hifavor, favor, opposed, hiopposed, title):
                plt.plot(hifavor[0], hifavor[1], 'go', label='Highly In Favor')
                plt.plot(favor[0], favor[1], 'yo', label='In Favor')
                plt.plot(opposed[0], opposed[1], 'mo', label='Opposed')
                plt.plot(hiopposed[0], hiopposed[1], 'ro', label='Highly Opposed')
                plt.title(title)
                plt.ylabel('Second Principal Component')
                plt.xlabel('First Principal Component')
                plt.legend(loc='upper left', numpoints=1)
                plt.show()

        #determine PCA projection
        pc1 = eigenvectors[:,0]
        pc2 = eigenvectors[:,1]
        x = np.dot(data.T, pc1)
        y = np.dot(data.T, pc2)

        #generate list of indices for various levels of support/opposition
        positionIndexMap = {}
        for index in range(len(sentiments)):
                key = sentiments[index][0]
                if key not in positionIndexMap:
                        positionIndexMap[key] = [index]
                else:
                        positionIndexMap[key].append(index)

        #classify x values according to support/opposition
        xhifavor = map(lambda index: x[index], positionIndexMap[1])
        xfavor = map(lambda index: x[index], positionIndexMap[2])
        xopposed = map(lambda index: x[index], positionIndexMap[3])
        xhiopposed = map(lambda index: x[index], positionIndexMap[4])

        #classify y values according to support/opposition
        yhifavor = map(lambda index: y[index], positionIndexMap[1])
        yfavor = map(lambda index: y[index], positionIndexMap[2])
        yopposed = map(lambda index: y[index], positionIndexMap[3])
        yhiopposed = map(lambda index: y[index], positionIndexMap[4])

        subplot((xhifavor, yhifavor),
                (xfavor, yfavor),
                (xopposed, yopposed),
                (xhiopposed, yhiopposed))

        fullplot((xhifavor, yhifavor),
                (xfavor, yfavor),
                (xopposed, yopposed),
                 (xhiopposed, yhiopposed), title)
        
def main():
        #get file handle
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

        #begin analysis
        datakeys = [keys.phone, keys.control, keys.internet, keys.social, keys.exclusion]
        IDs = ['PCA on Phone Category', 'PCA on Control Category', 'PCA on Internet category', 'PCA on Social Category', 'PCA on Exclusion Category']
        for index in range(len(datakeys)):
                key = datakeys[index]
                ID =  IDs[index]
                data = csv.generateMaskedArray(responseMap, key, maskValues)
                correlation = linalg.computeCorrelationMatrix(data, keys=key, log=True, path=basePath, keyname=ID)
                u, s, vt = linalg.computeSVD(correlation, log=True, path=basePath, keyname=ID)
                renderPCA(u, data, position, ID)

main()
