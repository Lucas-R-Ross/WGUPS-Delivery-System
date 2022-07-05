import copy


# The RouteBuilder manipulates the master distance adjacency matrix initialized by the Hub to create a specialized
# matrix that is used to determine the route a truck will take between its stops
class RouteBuilder:

    # nearest neighbor greedy algorithm that first marks any previously visited stops, then finds the stop with the
    # shortest distance in miles from the current stop
    #
    # time complexity = O(n^2), space complexity = O(n)
    @staticmethod
    def determineRoute(truck, distMatrix):

        # current location ID, used to update the truck's route as the route is built
        currentLocationID = 0

        # the corresponding float value in the distance matrix associated with the stop that was found to be closest
        # to the current stop
        nearestDist = 0

        # not the location ID, but the index position OF that location ID in the truck's list of route stops, used to
        # index the current adjacency matrix row with each new cycle of the loop
        nearestIndex = 0

        # list of index positions of locations that have already been visited
        visitedLocationIndexes = []

        while True:

            # a deep copy is needed because the original will need to be referenced after changes have been made to the
            # current row, and a shallow copy would result in a change in the copied row affecting the original as well
            currentLocationRow = copy.deepcopy(distMatrix[nearestIndex])

            # any previously visited locations are marked, so they will not be selected again
            for i in visitedLocationIndexes:
                currentLocationRow[i] = 0.0

            # the current location is added to the list of locations to be marked on next iteration
            visitedLocationIndexes.append(nearestIndex)

            # break out once all stops have been visited, taking the index position [0], since it corresponds with the
            # distance from the current location back to the Hub
            if len(visitedLocationIndexes) == len(currentLocationRow):
                nearestDist = distMatrix[nearestIndex][0]
                truck.route.append([currentLocationID, nearestDist])
                break

            # indexCounter will keep track of what the current index position is so that it can be stored in
            # nearestIndex when the nearest location is found in the current row
            indexCounter = 0

            # switch that skips the first iteration of the loop, since the first iteration will correspond with index
            # position 0, which is the Hub, which is where the truck already begins. The algorithm should not select
            # index 0 again as long as there are remaining unvisited stops
            nearestInitSwitch = 0

            for i in currentLocationRow:
                # all previously visited locations are marked at the start of each loop as '0.0', and the current row
                # will also have a value of 0.0 at the index mapping the distance to itself. To ensure these are never
                # selected, any 0.0 values are skipped over
                if i == 0.0:
                    indexCounter += 1
                    continue

                # nearest location is initialized to the first nonzero (valid, unvisited) value in the row, after which
                # it can be compared with subsequent values
                if nearestInitSwitch == 0:
                    nearestInitSwitch += 1
                    nearestDist = i
                    nearestIndex = indexCounter

                # the current distance to be compared is set to the value in the row at the current index
                currentDistance = i
                # if it is unvisited, and less than the previously assumed shortest distance, it is marked as the new
                # shortest
                if 0.0 < currentDistance < nearestDist:
                    nearestDist = currentDistance
                    nearestIndex = indexCounter
                indexCounter += 1

            # once the nearest neighboring location is determined, its location ID and corresponding distance are added
            # to the truck's route, which the truck will reference as it makes deliveries
            truck.route.append([currentLocationID, nearestDist])
            currentLocationID = truck.routeLocations[nearestIndex]

    # indexes the master adjacency matrix to create a specific distance matrix between all the stops a truck will
    # visit in its route
    #
    # time complexity = O(n^2), space complexity = O(n)
    @staticmethod
    def buildRouteAdjacencyMatrix(truck, distMatrix):
        routeAdjacencyMatrix = []
        # the numbers stored in each index position of the truck's route locations correspond to specific indexes
        # in the master adjacency matrix - these specific rows are pulled out to form the new matrix
        for i in truck.routeLocations:
            currentRow = distMatrix[i]
            adjustedRow = []
            for j in truck.routeLocations:
                adjustedRow.append(float(currentRow[j]))
            routeAdjacencyMatrix.append(adjustedRow)

        return routeAdjacencyMatrix
