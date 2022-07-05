from Clock import Clock


# truck objects will be used to facilitate the delivery of their associated packages by accounting for drive time
# between stops and updating package information upon delivery
class WGUPSTruck:
    truckID = int
    routeStartTime = int

    # truck's internal clock that allows for keeping track of route start time, package delivery time, and route
    # completion time
    currentTime = int

    timeOfReturn = int

    # original list of package objects is analyzed to find packages with same delivery location ID - and these are
    # grouped together and mapped in a dictionary
    pkgLocationMap = dict()

    # list containing the location IDs of the addresses the truck will visit on its route
    routeLocations = []

    # initialized to 0.0, and will keep track of truck's total miles on the route
    cumulativeMiles = float

    # 2d ordered list, where index[0] will specify the current location ID, and index[1] will specify the float value
    # in miles to the next stop. This is initialized by the RouteBuilder class before a truck begins its route
    route = []

    # reads index[1] of the current position in the truck route, adds that distance to the truck's cumulative miles,
    # moves the truck's clock forward by calculating the time taken to travel that distance, and then removes the prior
    # location from the truck's route
    #
    # time and space complexity = Big O(1)
    def driveToNextLocation(self):
        deliveryMiles = self.route[0][1]
        self.cumulativeMiles += deliveryMiles
        self.currentTime += round((deliveryMiles / 18) * 60)
        self.route.pop(0)

    # gets the packages to be delivered at the current stop from the truck's package-to-location map, marks them as
    # delivered and records the time at which delivery took place, and removes those packages from the truck
    #
    # time and space complexity = Big O(n)
    def deliverAtLocation(self):
        packagesAtCurrentStop = self.pkgLocationMap.get(self.route[0][0])
        for i in packagesAtCurrentStop:
            i.timeDelivered = self.currentTime
            i.status = "Delivered at " + Clock.convertIntToTime(i.timeDelivered)
        self.pkgLocationMap.pop(self.route[0][0])

    # when a truck completes its route and finishes driving back to the Hub, the time of return is marked, so it can
    # later be referenced by the dispatcher
    #
    # time and space complexity = Big O(1)
    def completeRoute(self):
        self.timeOfReturn = self.currentTime

    # for as long as there are remaining stops in the route to travel to, beginning at the Hub, the truck will drive to
    # the next stop, update its mileage and how long it took to get there, deliver its packages associated with that
    # stop, and repeat until it returns to the Hub and marks its time of return
    #
    # time and space complexity = Big O(n)
    def beginRoute(self):
        while True:
            self.driveToNextLocation()
            if not self.route:
                self.completeRoute()
                break
            self.deliverAtLocation()

    # truck is initialized with its ID number, and the time in minutes since midnight at which it will depart the Hub.
    # truck status and mileage will be dynamically calculated by the dispatcher at time of user query
    def __init__(self, truckNumber, startTime):
        self.truckID = truckNumber
        self.routeStartTime = startTime
        self.currentTime = startTime
        self.cumulativeMiles = 0.0
        self.routeLocations = []
