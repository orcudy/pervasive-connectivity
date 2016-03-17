import numpy as np
import csvutils as csv
import utils
import keys
import log

def correlation(dataMap, featureIDs, maskValues = []):
         dataArray = csv.generateArray(dataMap, featureIDs)
         mask = csv.generateDataMask(dataArray, maskValues)
         maskedArray = np.ma.masked_array(dataArray, mask)
         return np.ma.corrcoef(maskedArray)
         
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
        
        government = csv.generateArray(responseMap, keys.government)
        
        demographic = csv.generateArray(responseMap, keys.demographic + keys.government)
        phone = csv.generateArray(responseMap, keys.phone)
        quality = csv.generateArray(responseMap, keys.quality)
        control = csv.generateArray(responseMap, keys.control)
        internet = csv.generateArray(responseMap, keys.internet)
        social = csv.generateArray(responseMap, keys.social)
        exclusion = csv.generateArray(responseMap, keys.exclusion)

        
        #mask "Don't know" and "Refused" responses
        maskValues = [-1, 8, 9, 98, 99, 998, 999, 9998, 9999, 99999]
        np.set_printoptions(threshold=np.nan)
        corr = correlation(responseMap, keys.government + keys.demographic, maskValues)

        log.printArray(corr, '\t')



        
main()
		
