from Clock import Clock
from Hub import Hub


# the dispatcher responds to user queries from the main program interface, and displays current delivery environment
# statuses based on a given time
class Dispatcher:

    # displays package and truck status information at a given time
    #
    # time complexity = Big O(n), space complexity O(1)
    @staticmethod
    def getStatus(pkgID, requestedTime, pkgTable, trucks):
        requestedTime = Clock.convertTimeToInt(requestedTime)
        reportBorder = ""
        print("\nWGUPS Report at " + Clock.convertIntToTime(requestedTime) + ":\n " + reportBorder.ljust(253, '-'))

        # the requested package ID is used as a key into the master package hash table

        p = pkgTable.lookup(int(pkgID))

        # the user requested time is compared with significant times in the package data, such as time of delivery
        # and time of being loaded onto its truck - to determine the status of that package to display to the user
        if requestedTime < p.timeLoaded:
            p.setStatus("At Hub")
        elif p.timeLoaded <= requestedTime < p.timeDelivered:
            p.setStatus("En route on Truck " + str(p.truckLoadedOnto))
        elif requestedTime >= p.timeDelivered:
            p.setStatus("Delivered at " + Clock.convertIntToTime(p.timeDelivered) + " by Truck " +
                        str(p.truckLoadedOnto))
        currentPkgDeliveryDeadline = Clock.convertIntToTime(p.deliveryDeadline)

        # based on the data comparisons, the current status and info of the package are displayed to the user
        print("Package ID: " + str(p.pkgID).ljust(5) + "   " + "To: " + p.nameOnAddress.ljust(44) + "   " +
              "Address: " + p.address.ljust(38) + "   " + "City: " + p.city.ljust(18) + "   " + "State: " +
              p.state + "   " + "Zip: " + str(p.zip) + "   " + "Weight: " + str(p.mass).ljust(5) + "   " +
              "Delivery Deadline: " + currentPkgDeliveryDeadline.ljust(12) + "   " + "Status: " +
              p.status.ljust(40, " ") + p.notes)

        # after all package information has been printed, the 3 trucks are then examined. Similarly to how the
        # package statuses were determined, the status of each truck is displayed based on the comparison of the user
        # requested time and the significant times stored by the truck. The truck will display how many miles it has
        # accumulated over the course of its route, as well as its current status
        print("")
        totalMileage = 0.0
        for j in trucks:
            if requestedTime >= j.routeStartTime:
                if requestedTime >= j.timeOfReturn:
                    j.currentMileage = str(round(j.cumulativeMiles, 2))
                    truckStatus = "Route complete - returned to Hub at " + Clock.convertIntToTime(j.timeOfReturn)
                else:
                    j.currentMileage = str(round(((requestedTime - j.routeStartTime) / 60) * 18, 2))
                    truckStatus = "On delivery route - left Hub at " + Clock.convertIntToTime(j.routeStartTime)
                totalMileage += float(j.currentMileage)
            else:
                truckStatus = "At Hub - Not started delivery route"
                j.currentMileage = str(0.0)
            print("Truck " + str(j.truckID) + ":     Current mileage: " + j.currentMileage.ljust(10, ' ') + "          "
                  + "Status: " + truckStatus)

        # the mileage for all 3 trucks is added together to give the total mileage used by all trucks
        print("\nTotal mileage for all trucks at " + Clock.convertIntToTime(requestedTime) +
              ": " + str(round(totalMileage, 2)) + "\nEND OF REPORT\n" + reportBorder.ljust(253, '-'))
