import csv
from WGUPSPackage import WGUPSPackage
from PkgHashTable import PkgHashTable
from Clock import Clock


# the package initializer class reads package data from the package data csv file and stores it in WGUPSPackage objects.
# the objects are then inserted into a hash table where they can be retrieved using the package ID as a key
class PackageInit:

    # time and space complexity = Big O(n)
    @staticmethod
    def getPkgTable(locationIDMap, numPkgs):

        # csv file is opened and read in as a list of elements, where each element is a list containing each value
        # separated by commas per row in the file
        with open('PackageData.csv', 'r') as read_obj:
            pkgReader = csv.reader(read_obj)
            pkgInfoList = list(pkgReader)
            pkgObjs = PkgHashTable(numPkgs)

            # key counter designates the key that will be used to insert the package object into the hash table, and
            # increases by 1 with every loop through the csv file data
            keyCounter = 1
            for i in pkgInfoList:
                pkgID = int(i[0])
                adr = i[1]
                city = i[2]
                state = i[3]
                zc = i[4]
                deadline = Clock.convertTimeToInt(i[5])
                massKG = i[6]
                note = i[7]

                # locationIDMap is initialized in LocationsInit. It maps addresses to a corresponding name and ID number
                # which are then stored in the package object
                locID = locationIDMap.get(adr)[0]
                adrName = locationIDMap.get(adr)[1]

                # all stored data is used to construct a new package object, which is then paired with a key
                # representing that package's ID number, and placed in a hash table
                pkgObjs.insert(keyCounter, WGUPSPackage(adrName, pkgID, adr, locID, city, state, zc, deadline, massKG,
                                                        note))
                keyCounter += 1

        return pkgObjs
