# Direct Hash Table being used, with a resize if more packages are added than there are room for.
class DirectHashTable:

    """
    Based off of direct hash table in ZyBooks chapter 7 section 7.
    Creates the hash table with 41 buckets to accommodate the direct hashing of 40 packages. This can be altered to
    start with different numbers of packages by changing the capacity, or can leave the capacity alone and the resize
    will be done automatically when a package id of 41 or higher is used.
    The big O time complexity of this is O(1), because there are a known number of iterations for the for loop, and
    the rest of the operation have a time complexity of O(1).
    The big o space complexity is O(N) with n being the number of packages.
    """

    def __init__(self, capacity=41):
        self.buckets = []
        self.capacity = capacity
        for i in range(self.capacity):
            self.buckets.append([])

    """
    This method is used to add a package to the proper bucket in the list of buckets. It is put in the bucket 
    corresponding to it's package id number.
    The Big O time complexity of this method is O(N), it could be O(1) for the single operation if the package being 
    added is already in the range of the available capacity. However, if the resize method is called it becomes O(N), 
    because that is the time complexity of the resize.
    The space complexity is O(N), because it is a direct hash and requires a bucket for every package being stored.
    """
    def add(self, package):
        if package.id >= self.capacity:
            self.resize(package.id)
        self.buckets[package.id] = package

    """
    The search method takes an integer id number and searches the hash table for that package id number. Using direct
    hashing, it checks the bucket number of the id number, if there is a package there it returns the package, or none
    if there isn't a package with that id number.
    This has a Big O space and time complexity of O(1), because it takes one operation to access the bucket to see if 
    there is a package. 
    """
    def search(self, id_number):
        if self.buckets[id_number] is not None:
            return self.buckets[id_number]
        else:
            return None

    """
    The remove method checks to see if the supplied package is in the range of the available capacity, if it is it sets
    the bucket to empty.
    This has a Big O space and time complexity of O(1), because it takes one operation to check if it is in range, 
    and one operation to set the bucket to empty if it is. With both being constants the Big O is O(1).
    """
    def remove(self, package):
        if package.id < self.capacity:
            self.buckets[package.id] = []

    """
    This method automatically resizes the direct hash table if a package is added with an id higher than the capacity.
    This method is called by add method when the resize is required. First it copies the buckets. Then, it increases 
    the capacity till the capacity is greater than the supplied id number. Then it remakes the buckets using the new 
    capacity. Finally it copies the packages that were in the old buckets to the new buckets. 
    The Big O time complexity of this method is O(N). The while loop runs O(N) number of time depending on the 
    package that is added. The first for loop runs O(N) number of times because the number of capacity is unknown 
    till the new package is added. The second for loop runs O(N) number of times because the previous capacity is 
    unknown when it is run during the program. The rest of the operations are O(1), leaving the final complexity at 
    O(N).
    The space complexity is O(N), requiring a bucket for every package.
    """
    def resize(self, id_number):
        temp_buckets = self.buckets
        while id_number >= self.capacity:
            self.capacity *= 2
        self.buckets = []
        for i in range(self.capacity):
            self.buckets.append([])
        for i in range(len(temp_buckets)):
            self.buckets[i] = temp_buckets[i]
