# the package hash table maps package objects storing data to a key representing that package's ID number. This way,
# particular packages, such as the one with an incorrect address, or a list of packages to be loaded on a specific
# truck, can be quickly and easily accessed
#
#
# The following video resource was referenced in the creation of this hash map:
# Joe James. (2016, January 23). Python: Creating a HASHMAP using Lists [Video]. YouTube.
# https://www.youtube.com/watch?v=9HFbhPscPU0&ab_channel=JoeJames
#
# benefit of hash table is all method actions (inserting, lookup, deletion, etc) are O(1) time and space complexity
class PkgHashTable:

    length = int
    map = []

    # the table is initialized with a number of empty slots equal to the number of packages being delivered, which
    # is specified by the Hub
    def __init__(self, size):
        self.length = size
        self.map = [None] * self.length

    # to ensure the hash for the associative array is within the bounds, the modulo of the size is taken in relation to
    # the given key
    def getHash(self, key):
        return key % self.length

    # inserts a given key value pair at an index corresponding to the key, where it can then be reached using the key
    def insert(self, key, value):

        # the key input is hashed to get an index position to place the requested data
        keyHash = self.getHash(key)

        # the 2 input data are stored together in a list that will be placed in the keyHash index position
        keyValuePair = [key, value]
        self.map[keyHash] = keyValuePair

    # retrieves a value (in the case of this program, a package object) at a given key by indexing the list at the
    # hash of the key, and returning the value in the [key, value] pair at that index. returns None if nothing has
    # been inserted at that index
    def lookup(self, key):
        keyHash = self.getHash(key)
        if self.map[keyHash]:
            return self.map[keyHash][1]
        return None
