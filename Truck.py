"""
This class contains the delivery truck information.
"""
import datetime


class Truck:
    """
    This is the initializer for the truck objects, with predefined information saved in for each truck.
    This has a Big O time complexity of O(1), with 5 single operations.
    """
    def __init__(self):
        self.miles_driven = 0
        self.loaded_packages = []
        self.departure_time = datetime.timedelta(hours=8, minutes=0, seconds=0)
        self.last_delivery_time = datetime.timedelta(hours=8, minutes=0, seconds=0)
        self.returned_from_run = False

    """
    This method sets the departure time for the truck that is supplied. This also sets the last delivery time to the 
    same time as the departure time.
    This has a Big O space and time complexity of O(1), with 2 single operations.
    """
    def set_departure_time(self, departure_time):
        self.departure_time = departure_time
        self.last_delivery_time = self.departure_time

    """
    This method updates the last delivery time using the supplied delivery time.
    This has a Big O space and time complexity of O(1).
    """
    def update_last_delivery_time(self, delivery_time):
        self.last_delivery_time = delivery_time

    """
    This method updates the miles that a truck has driven after a package has been delivered.
    The Big O space and time complexity is O(1).
    """
    def update_miles(self, miles):
        self.miles_driven += miles

    """
    This method sets the returned from run variable to true after the truck has returned to the hub.
    The Big O space and time complexity is O(1).
    """
    def update_returned_from_run(self):
        self.returned_from_run = True

    """
    This method is used to reset the trucks after a requested simulation has finished to be prepared for the next 
    simulation.
    The Big O space and time complexity is O(1)
    """
    def reset_truck(self):
        self.miles_driven = 0
        self.loaded_packages = []
        self.departure_time = datetime.timedelta(hours=8, minutes=0, seconds=0)
        self.last_delivery_time = datetime.timedelta(hours=8, minutes=0, seconds=0)
        self.returned_from_run = False
