"""
This is the package class containing all the information for the various packages that will be loaded on the trucks.
"""


class Package:
    """
    This is the initializer for the package class, taking the supplied information and saving them.
    This has a Big O space and time complexity of O(1), with there being 8 single operation becoming one in big o
    notation.
    """
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, special_notes,
                 delivery_status):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status

    """
    This defines how the package will be displayed when it is printed to the terminal.
    """
    def __str__(self):
        return (f'{self.id:>4} | {self.address:<45} | {self.city:<20} | {self.state:>5} | {self.zip:>5} |'
                f' {self.weight:<6} | {self.delivery_deadline:<8} | {self.delivery_status}')

    """
    This method is used to change the delivery status of a package to the name of the truck that delivered the 
    package and the time it was delivered at.
    This has a Big O time complexity of O(1), with one operation.
    """
    def package_delivered(self, delivery_time, delivery_truck):
        self.delivery_status = delivery_truck + (' delivered at: ' + str(delivery_time))

    """
    This method sets the delivery status of a package, with the provided delivery status.
    This has a Big O time complexity of O(1), with one operation.
    """
    def set_delivery_status(self, status):
        self.delivery_status = status

    """
    This method changes the delivery address of a package, using the supplied address information.
    This has a Big O space and time complexity of O(1).
    """
    def change_delivery_address(self, address, city, state, zipcode):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zipcode
