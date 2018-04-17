"""
    Retrieve data module for IR system

    Use function loadData to:

        1. download json data from URL
        2. Save data in a local gz file
        3. Load data into the program 
"""

import urllib2
import gzip
import json
import os

# Source Url 
url = "https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/software-engineer/products.json.gz"

# local json file
gzFile = './products.json.gz'
# index file (used by index module)
indexFile = './products.p'

def downloadData(url, dst):
    """ Download data and save it locally """
    print("Downloading json file...")
    filedata = urllib2.urlopen(url)  
    data = filedata.read()
    with open(dst, 'wb') as f:  
        f.write(data)
        f.close()

def deleteFiles(files):
    """ Delete a list of files """
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

def loadData():
    """ Load data into the program. 

    Get data locally if gz file exists. If not, download it from URL 
    and delete indexFile (to force rebuild)

    # Returns: 
        list of records
    """

    if not os.path.isfile(gzFile):
        downloadData(url, gzFile)
        deleteFiles([indexFile])

    with gzip.GzipFile(gzFile, 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))
        print("%d products in DB."%(len(data)))
        return data
    raise IOError("Error loading %s"%(gzFile))

def printDataMeta(data):
    """Shows meta-information of data"""
    print("%d products in DB."%(len(data)))
    print("Type of line0: %s." %(type(data[0])))
    print("Fields: %s." % (data[0].keys()))


def test():
    """Basic testing of this module"""
    print("Testing Retrieve Data...")
    # force remote fetch and index build
    deleteFiles([gzFile, indexFile])
    data = loadData()  
    printDataMeta(data)


if __name__ == "__main__":
    test()