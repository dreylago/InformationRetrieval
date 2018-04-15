"""
    Index module for IR system

    Use the function run to load (or build) index file and print metadata.

"""

from future.utils import iteritems
import retrieve_data as rd
import index

def test():
    """Basic testing of module"""
    print("Testing Index...")
    data = rd.loadData()
    dataIndex = index.run(data)
    index.printIndexDebug(dataIndex)

if __name__ == "__main__":
    test()