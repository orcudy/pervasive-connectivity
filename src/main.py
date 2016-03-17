import numpy as np
import csvutils as csv
import utils

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
        
        demographicKeys = ['sex',
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
        
        demographics = csv.generateArray(responseMap, demographicKeys)
        np.set_printoptions(threshold=np.nan)
        print demographics.shape
        print demographics


        
main()
		
