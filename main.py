# Lucas Ross
# Student ID: 009968598
#
# Welcome to WGUPS time reporting service. This program consists of 10 code files and 3 csv data files, whose purpose
# and functionality are outlined below.
#
# Code Files:
#
#   1. main.py  -  The program entry point. Main's job is to initialize the environment by calling the Hub's
#                  startup method, and to take in user input at the program menu. Once the data has been verified as
#                  valid, the Dispatcher class is called to act upon it.
#
#   2. Hub.py  -   The Hub class contains methods for initializing the delivery environment. The Hub is responsible
#                  for storing the data read from csv files, specifying the packages to be loaded onto each truck,
#                  initializing, loading, and sending off trucks, and specifying the total number of packages to be
#                  delivered.
#
#   3. Dispatcher.py   -   The dispatcher responds to user queries from the main program interface, and displays current
#                           delivery environment statuses based on a given time
#
#   4. WGUPSTruck.py   -   This is the blueprint from which to build truck objects, which facilitate the delivery
#                          of packages loaded onto them. Trucks are responsible for internally keeping track of the
#                          times at which they start and end their routes, as well as the time of each package delivery.
#
#   5. RouteBuilder.py   -   The core algorithm of the program that determines the order in which a truck will visit
#                            the locations on its route.
#
#   6. WGUPSPackage.py   -   Blueprint for package objects - which are simply containers for storing package data
#
#   7. Clock.py   -   The clock converts between integer and human-readable string representations of time, and is also
#                     responsible for asserting properly formatted time input from the user.
#
#   8. PkgHashTable.py   -   Blueprint for building the hash table object that is used to store package objects
#
#   9. PackageInit.py   -   The package initializer class reads package data from the package data csv file and stores
#                           it in WGUPSPackage objects.
#
#   10. LocationsInit.py   -   The locations initializer class has two responsibilities - to initialize the data
#                              structure mapping an address to its location ID, and to initialize the master adjacency
#                              matrix
#
# Data Files:
#
#   1. DistanceTable.csv   -   Matrix mapping every delivery location to every other using a list of floating point
#                              distance values
#
#   2. PackageData.csv   -   File containing data relevant to each package. This data is read and stored in package
#                            objects.
#
#   3. DeliveryNamesAndAddresses.csv   -   File mapping addresses to addressee names and location IDs, which is used
#                                          to populate package objects' delivery locationID field.
#
#
#
#   Overall program time complexity is O(n^2), and overall space complexity is O(n). Please see class and
#   method-specific comments for space-time complexities of individual code blocks.

from Clock import Clock
from Hub import Hub
from Dispatcher import Dispatcher


# program entry
#
# since this method encompasses the entire life of the program, time complexity of this method is the time complexity
# of the overall program - which is Big O(n^2). Space complexity is also that of the entire program - O(n).
def runProgram():

    # initialize the packages and locations by reading the csv files, load packages onto trucks,
    # determine routes for trucks to take based on package delivery locations, and have trucks execute their routes
    Hub.startDeliveryDay()
    programUIBorder = ""
    print("\n" + programUIBorder.ljust(100, '*') + "\nWelcome to WGUPS Daily Time Reports!")

    # main menu - program will loop to allow for multiple queries until user enters 'x' to break out
    while True:
        pkgToCheck = input("\nPlease enter the numeric ID of the package you would like to check (1-" +
                           str(Hub.numTotalPackages) + ") or enter 'x' to exit: ")
        while (not pkgToCheck.isdigit() or not 0 < int(pkgToCheck) < 41) and not pkgToCheck.casefold() == "x":
            pkgToCheck = input("\nError - please input valid numeric ID 1-" + str(Hub.numTotalPackages) + ": ")

        if pkgToCheck.casefold() == "x":
            break

        userTime = input("\nPlease enter a time in format 'H:MM <AM/PM>' (eg. '11:06 AM') or enter 'x' to exit: ")\
            .lstrip()
        while not Clock.getValidInput(userTime) and not userTime.casefold() == "x":

            # input must be valid to be parsed correctly - will assert properly formatted input from user
            userTime = input("Error - please enter a valid time in format H:MM <AM/PM> (eg. '1:27 PM'): ").lstrip()
        if userTime.casefold() == "x":
            break
        # upon receiving valid time input, the dispatcher is called to retrieve data for all packages at that time
        Dispatcher.getStatus(pkgToCheck, userTime, Hub.masterPkgTable, Hub.trucks)

    print("\nThank you for using our service!\n" + programUIBorder.ljust(100, '*'))


runProgram()
