# the package class is used to instantiate package objects that store the data relevant to a particular package.
# these packages objects are placed in the master package hash table, where they can be easily located by their
# ID numbers, and can be passed to other objects and manipulated further
class WGUPSPackage:
    pkgID = int
    nameOnAddress = str
    address = str
    city = str
    state = str
    zip = str
    deliveryLocationID = int
    deliveryDeadline = int
    mass = int
    notes = str
    timeDelivered = int
    timeLoaded = int
    truckLoadedOnto = int
    status = str

    # no get / set methods needed for these - with exception to status, they do not change
    def __init__(self, name, pid, adr, locID, cit, sta, zc, dd, kg, note):
        self.nameOnAddress = name
        self.pkgID = pid
        self.address = adr
        self.city = cit
        self.state = sta
        self.zip = zc
        self.deliveryLocationID = locID
        self.deliveryDeadline = dd
        self.mass = kg
        self.notes = note
        self.status = "At Hub"

    # set status used by dispatcher to assign proper status based on user time query
    def setStatus(self, status):
        self.status = status
