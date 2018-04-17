"""
    Prints Index Histogram

"""

from index import *
from retrieve_data import *

data = loadData()
dataIndex = run(data)
printIndexDebug(dataIndex)
