from RouteBuilder import RouteBuilder
from PackageInit import PackageInit
from LocationsInit import LocationsInit
from WGUPSTruck import WGUPSTruck


# abstract class containing methods for initializing delivery environment
class Hub:
    # initializes the master adjacency matrix from the distances csv file - which will be used to associate a distance
    # in miles between every stop to every other stop and thus enable an efficient route to be determined
    masterDistanceList = LocationsInit.initMasterAdjacencyMatrix()

    # initializes the location ID map - which maps every delivery address to a location ID and location name. This map
    # will in turn be used to initialize packages
    locationIDMap = LocationsInit.getLocationIDMap()

    # the number of packages to be delivered, which dictates the size of the hash table that will store the package
    # objects
    numTotalPackages = 40

    # initializes the Package Hash table, which will map package ID numbers with a corresponding Object to store that
    # package's data
    masterPkgTable = PackageInit.getPkgTable(locationIDMap, numTotalPackages)

    # used to assert that a list of packages being loaded onto a truck is of an allowable size
    numPkgsAllowedPerTruck = 16

    # list of the truck objects - this will later be used by the dispatcher to determine the status of the trucks at a
    # given time
    trucks = []

    # algorithmic sorting not a requirement - so these are hard coded. From here, they can be easily moved from one
    # truck to another, or additional packages can be added - based on package delivery requirements
    truck1Packages = [8, 10, 13, 14, 15, 16, 19, 20, 21, 27, 29, 30, 34, 35, 37, 39]
    truck2Packages = [1, 2, 3, 4, 5, 6, 7, 9, 17, 18, 31, 32, 33, 36, 38, 40]
    truck3Packages = [11, 12, 22, 23, 24, 25, 26, 28]

    # the 3 trucks are initialized with their ID number and the time in minutes since midnight at which they will
    # begin their routes. Each truck is then loaded with its designated package objects, and begins its route.
    #
    # time and space complexity = Big O(n)
    @staticmethod
    def startDeliveryDay():
        truck1 = WGUPSTruck(1, 480)
        Hub.trucks.append(truck1)
        Hub.loadTruck(truck1, Hub.createTruckPkgList(Hub.truck1Packages))
        Hub.dispatch(truck1)

        truck2 = WGUPSTruck(2, 545)
        Hub.trucks.append(truck2)
        # one of the packages has an incorrect address, and it is given that the shipping company is both aware of the
        # mistake, and when it will be corrected. The only requirement is that it cannot be delivered at its correct
        # address before 10:20 AM. Thus, the correction is made with the proper address before delivery.
        Hub.fixWrongAddresses(9)
        Hub.loadTruck(truck2, Hub.createTruckPkgList(Hub.truck2Packages))
        Hub.dispatch(truck2)

        # because there are 3 trucks but only 2 drivers, the 3rd truck must not begin its route until the first truck
        # completes its route and returns to the Hub
        truck3 = WGUPSTruck(3, truck1.timeOfReturn)
        Hub.trucks.append(truck3)
        Hub.loadTruck(truck3, Hub.createTruckPkgList(Hub.truck3Packages))
        Hub.dispatch(truck3)

    # the truck's package number list is iterated through as keys into the package hash table, and the values in the
    # table - ie - the associated package objects, are put in a list and stored in the truck
    #
    # time and space complexity = Big O(n)
    @staticmethod
    def createTruckPkgList(idList):

        # ensures no more than the allowable number of packages are loaded on a truck
        assert len(idList) <= Hub.numPkgsAllowedPerTruck
        packagesForTruck = []
        for i in idList:
            packagesForTruck.append(Hub.masterPkgTable.lookup(i))
        return packagesForTruck

    # the incorrect address is updated in the package hash table before being sent off for delivery
    #
    # time and space complexity = Big O(1)
    @staticmethod
    def fixWrongAddresses(incorrectAddressPkgID):
        pkgToBeUpdated = Hub.masterPkgTable.lookup(incorrectAddressPkgID)

        pkgToBeUpdated.nameOnAddress = "Third District Juvenile Court"
        pkgToBeUpdated.address = "410 S State St"
        pkgToBeUpdated.city = "Salt Lake City"
        pkgToBeUpdated.zip = "84111"
        pkgToBeUpdated.state = "UT"
        pkgToBeUpdated.notes = "Previously incorrect address - corrected at 10:20 AM"
        pkgToBeUpdated.deliveryLocationID = 19

    # once the correct package objects for a truck have been retrieved from the package hash table into a list, the list
    # is iterated through, and for each package object, the package's status is updated from "At Hub" to "En route",
    # its associated truck is initialized to the ID of the current truck being loaded, and the time at which the
    # package is loaded is initialized to the truck's route start time
    #
    # time and space complexity = Big O(n)
    @staticmethod
    def loadTruck(truck, pkgList):
        for i in pkgList:
            i.truckLoadedOnto = truck.truckID
            i.timeLoaded = truck.routeStartTime
            i.status = "En route"

            # after the data for the current package is updated, the packages are grouped together if they have the
            # same delivery address. That way, a truck associates all packages at one stop with the same location ID,
            # and no stop is unnecessarily visited more than once
            if i.deliveryLocationID in truck.pkgLocationMap.keys():
                truck.pkgLocationMap.get(i.deliveryLocationID).append(i)
            else:
                currentLocationPkgList = [i]
                locationIDKey = i.deliveryLocationID
                truck.routeLocations.append(locationIDKey)
                truck.pkgLocationMap.update({locationIDKey: currentLocationPkgList})

        # the Hub has a location ID of 0, which is used to initialize the list of location IDs the truck will visit
        # on its route
        truck.routeLocations.append(0)
        truck.routeLocations.sort()

        # now that the truck is loaded with its packages and the location IDs it will visit have been determined, these
        # data can be used to determine the proper indexes into the master adjacency list between stops
        # to create a smaller adjacency matrix specific to the current truck's route
        truckDistMatrix = RouteBuilder.buildRouteAdjacencyMatrix(truck, Hub.masterDistanceList)

        # following creation of the adjacency matrix, the matrix is then used by the route builder to determine the
        # efficient route the truck will take between all of its stops
        RouteBuilder.determineRoute(truck, truckDistMatrix)

    # once a truck is loaded and its route has been determined, it is ready to begin its deliveries
    # time and space complexity = Big O(n)
    @staticmethod
    def dispatch(truck):
        truck.beginRoute()
