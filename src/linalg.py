import numpy as np
import csvutils as csv

def computeCorrelationMatrix(data, keys=[], log=False, path='', keyname=''):
        correlation = np.ma.corrcoef(data)
        if log and path and keyname:
                corr_path = path + '/' + keyname + '_corr.csv'
                csv.writeToCSV(correlation, corr_path, [''] + keys, keys)
        return correlation
                        
def computeSVD(data, keys=[], log=False, path='', keyname=''):        
        u, s, vt = np.linalg.svd(data)
        if log and path and keyname:
                svd_path = path + '/' + keyname + '_svd.csv'
                csv.writeToCSV(u, svd_path, [], keys)
        return u, s, vt
        
