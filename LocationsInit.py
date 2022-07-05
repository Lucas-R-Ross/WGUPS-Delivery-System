import copy
import csv


# the locations initializer class has two responsibilities - to initialize the data structure mapping an address to its
# location ID, and to initialize the master adjacency matrix. These tasks are accomplished by reading the relevant csv
# files and storing the resulting data
class LocationsInit:

    # this method returns a dictionary mapping an ID, name pair to an address key
    #
    # time and space complexity = O(n)
    @staticmethod
    def getLocationIDMap():

        # the 'with' keyword ensures that the file stream will be automatically closed once reading is complete
        with open('DeliveryNamesAndAddresses.csv', 'r') as read_obj:
            addressReader = csv.reader(read_obj)

            # the csv is read in as a list of pairs - each pair consisting of a name, address
            addressList = list(addressReader)
            locationIDMap = dict()

            # the locationID counter keeps track of the index of what is being read in from the file, and is used to
            # represent a location's ID when it is inserted in the table for each loop iteration
            locationID = 0
            for i in addressList:
                locationIDMap.update({i[1]: [locationID, i[0]]})
                locationID += 1
        return locationIDMap

    # the given DistanceTable file is only 'half' filled in - this method 'mirrors' it to create a full square matrix -
    # meaning each stop can be associated with every other stop. This master matrix is used by the route builder and
    # indexed at specific locations to help determine a truck's route
    #
    # time complexity = O(n^2), space complexity = O(n)
    @staticmethod
    def initMasterAdjacencyMatrix():
        with open('DistanceTable.csv', 'r') as read_obj:
            distanceReader = csv.reader(read_obj)
            distancesList = list(distanceReader)
            fullDistanceMatrix = []

            for i in distancesList:

                # each element in the distancesList is a list of float values representing distances to other stops
                # from the current stop - the ID of the current stop is determined by the index position of the list -
                # which is the same as the indexes from the locationID map
                currentLocationRow = copy.deepcopy(i)

                # in each current row, the current location index is the number of distance values in the list - 1,
                # since indexing begins at 0 not 1
                currentLocationIndex = (len(i) - 1)

                # the index to start reading additional values from, to append onto the current list - should be
                # the next index, or + 1 from the current
                startingIndex = currentLocationIndex + 1

                # as long as the current row is not the last row and there are additional rows after the current
                # from which to append new values onto this list, each list will be indexed for the distance value
                # to add
                if len(distancesList) >= (startingIndex + 1):

                    # for every index of the list read in from the file, in other words, for every location's list
                    # of distances to other stops, the index position of the current stop is determined, and that index
                    # is used to index every other list in the same position, adding on the distance value at that
                    # position to the current list. This 'fills in' the matrix - all data mapping each location to
                    # every other is already present in the file - it just needs to be reorganized.
                    for j in distancesList:
                        if len(j) <= startingIndex:
                            continue
                        currentLocationRow.append(j[currentLocationIndex])
                fullDistanceMatrix.append(currentLocationRow)

        return fullDistanceMatrix
