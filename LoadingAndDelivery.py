"""
This class is responsible for loading the package data into the hashtable, the distance data into the adjacency
matrix and the matrix key list. Also, this class then loads the trucks using a prioritized nearest neighbor
algorithm. Finally, this class runs the delivery simulations that are requested by the user using the command prompt
user interface.
"""
import Truck
import Package
import HashTable
import csv
import datetime


class LoadingAndDelivery:
    # The three delivery trucks.
    truck_1 = Truck.Truck()
    truck_2 = Truck.Truck()
    truck_3 = Truck.Truck()
    # Package hash table using the Hash Table class.
    package_hash_table = HashTable.DirectHashTable()
    # Truck speed in miles per second.
    truck_speed = 0.005
    # Adjacency matrix containing the distances between nodes.
    distance_adjacency_matrix = []
    for i in range(27):
        distance_adjacency_matrix.append([])
    # Key for the adjacency matrix.
    distance_adjacency_key = []

    """
    This initializes the Loading and Delivery class objects, executing the load_package_data, load_distance_data, 
    and load_trucks_set_departure functions utilizing the provided package file and distance file.
    """
    def __init__(self, package_filename, distance_filename):
        self.load_package_data(package_filename)
        self.load_distance_data(distance_filename)
        self.load_trucks_set_departure()

    """
    This method loads the pacakge data into the package hash table.
    The Big O runtime complexity is O(N), with the for loop running once for each package in the file.
    The Big O space complexity is O(N), because the hash table that everything is loaded into has a space complexity 
    of O(N).
    """
    def load_package_data(self, filename):
        with open(filename) as packages:
            package_data = csv.reader(packages, delimiter=',')
            next(package_data)
            for package in package_data:
                package_id = int(package[0])
                address = package[1]
                city = package[2]
                state = package[3]
                zip_code = package[4]
                delivery_deadline = package[5]
                weight = int(package[6])
                notes = package[7]
                if notes == 'Delayed on flight---will not arrive to depot until 9:05 am':
                    delivery_status = 'in route to hub'
                else:
                    delivery_status = 'at hub'
                new_package = Package.Package(package_id, address, city, state, zip_code, delivery_deadline, weight,
                                              notes, delivery_status)
                self.package_hash_table.add(new_package)

    """
    This method loads the distances into the distance adjacency matrix and the address keys into the key list.
    This has a Big O time complexity of O(N^2), because it has to go through N rows and N columns to add all of the 
    data to the adjacency matrix.
    This has a Big O space complexity of O(N^2), because it is a nested list that has N indices, each index having a 
    list with N indices. The adjacency key list has O(N) for space complexity so the final complexity ends up being 
    O(N^2).
    """
    def load_distance_data(self, filename):
        with open(filename) as distances:
            distance_data = csv.reader(distances, delimiter=',')
            current_row = 0
            next(distance_data)
            for distance in distance_data:
                self.distance_adjacency_key.append(distance[0])
                for i in range(27):
                    cell = i + 1
                    self.distance_adjacency_matrix[current_row].append(distance[cell])
                current_row += 1

    """
    This method is used to print all of the packages in the package hash table.
    This has a Big O time complexity of O(N), because it has to go through N packages and print them all.
    This has a Big O space complexity of O(1).
    """
    def print_all_packages(self):
        print('{:2>4} | {:<45} | {:<20} | {:>5} | {:>5} | {:<6} | {:<8} | {}'.format('ID', 'Address', 'City',
                                                                                     'State', 'Zip', 'weight',
                                                                                     'Deadline', 'Status'))
        for i in range(self.package_hash_table.capacity - 1):
            print(self.package_hash_table.search(i + 1))

    """
    This method takes in the number of miles driven and returns how long it will take using the miles per second speed.
    This has a Big O space and time complexity of O(1).
    """
    def time_taken(self, miles):
        hours = 0
        minutes = 0
        seconds = miles / self.truck_speed

        if seconds >= 60:
            minutes = seconds / 60
            seconds = seconds % 60
        if minutes >= 60:
            hours = minutes / 60
            minutes = minutes % 60

        return int(hours), int(minutes), int(seconds)

    """
    This method takes two locations and finds them in the adjacency key and then uses the two index values to get the 
    miles between the two locations.
    This has a Big O time complexity of O(N), because it has to search the list for the supplied address, 
    which it might have to go through the entire list to find it making it O(N). Whereas using the indexes from the key 
    you search 2 possible locations in the adjacency matrix making that part O(1). 
    """
    def distance_between_nodes(self, location_1, location_2):
        index_1 = self.distance_adjacency_key.index(location_1)
        index_2 = self.distance_adjacency_key.index(location_2)

        if self.distance_adjacency_matrix[index_1][index_2] == '':
            return float(self.distance_adjacency_matrix[index_2][index_1])
        else:
            return float(self.distance_adjacency_matrix[index_1][index_2])

    """
    This method takes a package and converts the address of the pacakge and the zip from the package into the key for 
    the adjacency list.
    This has a Big O space and time complexity of O(1).
    """
    def convert_package_to_key(self, package):
        key_string = package.address + ' ' + '(' + package.zip + ')'
        return key_string

    """
    nearest_neighbor algorithm based off of (Weru, 2021).
    This method finds the next closes package to deliver when supplied with the starting package, a list of possible 
    next packages, and a code telling if the the truck is just leaving the hub so it can use 'HUB' as the adjacency key.
    This has a Big O time complexity of O(N), it has to go through every package in the package list to make sure it 
    chooses the closest next delivery.
    This has a Big O space complexity of O(N), for the package list being used.
    """
    def nearest_neighbor(self, starting_package, package_list, code):
        distance = 140.0
        closest_index = -1
        if code == 'HUB':
            for i in range(len(package_list)):
                temp_distance = self.distance_between_nodes('HUB', self.convert_package_to_key(
                    self.package_hash_table.search(package_list[i])))
                if temp_distance < distance:
                    closest_index = i
                    distance = temp_distance
        else:
            for i in range(len(package_list)):
                temp_distance = self.distance_between_nodes(self.convert_package_to_key(starting_package),
                                                            self.convert_package_to_key(
                                                                self.package_hash_table.search(package_list[i])))
                if temp_distance < distance:
                    closest_index = i
                    distance = temp_distance
        return closest_index

    """
    This method takes three lists of packages with different priority levels, the truck they will be loaded on, 
    and the estimated departure time of the truck and loads those packages on the truck. It starts by loading all of 
    the level one priority packages, followed by level two and finally all of the level three packages using the 
    nearest_neighbor function to pick the next package to load.
    This has a Big O time complexity of O(N^2), because it has to go through each package making this function O(N), 
    then it sends it to the nearest neighbor function which is also O(N), making it O(N) * O(N) = O(N^2).
    The Big O space complexity is O(N) for the N number of packages in the lists.
    """
    def priority_load_with_nearest_neighbor(self, level_one_priority, level_two_priority, level_three_priority,
                                            truck, depart_time):
        last_loaded = None

        while len(level_one_priority) > 0 or len(level_two_priority) > 0 or len(level_three_priority) > 0:
            if last_loaded is None:
                code = 'HUB'
            else:
                code = 'No code'
            if len(level_one_priority) != 0:
                index_to_load = self.nearest_neighbor(last_loaded, level_one_priority, code)
                package_to_load = self.package_hash_table.search(level_one_priority.pop(index_to_load))
                truck.loaded_packages.append(package_to_load)
                last_loaded = package_to_load
                continue
            if len(level_two_priority) != 0:
                index_to_load = self.nearest_neighbor(last_loaded, level_two_priority, code)
                package_to_load = self.package_hash_table.search(level_two_priority.pop(index_to_load))
                truck.loaded_packages.append(package_to_load)
                last_loaded = package_to_load
                continue
            if len(level_three_priority) != 0:
                index_to_load = self.nearest_neighbor(last_loaded, level_three_priority, code)
                package_to_load = self.package_hash_table.search(level_three_priority.pop(index_to_load))
                truck.loaded_packages.append(package_to_load)
                last_loaded = package_to_load
                continue
        truck.set_departure_time(depart_time)

    """
    This method loads specific packages onto the trucks utilizing priority_load_with_nearest_neighbor, 
    and the nearest_neighbor methods. It passes the priority package lists to the method and the trucks are loaded 
    with a priority nearest neighbor.
    The Big O time complexity is O(N^2) because it calls the priority_load_with_nearest_neighbor method three times.
    The Big O space complexity is O(N) for the number of packages in the lists.
    """
    def load_trucks_set_departure(self):
        level_one_priority = [15]
        level_two_priority = [1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40]
        level_three_priority = [19, 21, 24]
        depart_time = datetime.timedelta(hours=8, minutes=0, seconds=0)
        self.priority_load_with_nearest_neighbor(level_one_priority, level_two_priority, level_three_priority,
                                                 self.truck_1, depart_time)

        level_one_priority = []
        level_two_priority = [6, 25]
        level_three_priority = [3, 4, 8, 10, 11, 17, 18, 23, 28, 32, 33, 36, 38]
        depart_time = datetime.timedelta(hours=9, minutes=5, seconds=0)
        self.priority_load_with_nearest_neighbor(level_one_priority, level_two_priority, level_three_priority,
                                                 self.truck_2, depart_time)

        level_one_priority = []
        level_two_priority = []
        level_three_priority = [2, 5, 7, 9, 12, 22, 26, 27, 35, 39]
        depart_time = datetime.timedelta(hours=10, minutes=20, seconds=0)
        self.priority_load_with_nearest_neighbor(level_one_priority, level_two_priority, level_three_priority,
                                                 self.truck_3, depart_time)
    """
    This method takes a user entered time, a possible package number, and a code to run the delivery simulation. It 
    delivers packages that are delivered before the time entered by the user, and returns the report that the user 
    requested for the delivery status and miles of the deliveries.
    This has a Big O time complexity of O(N^2), because it resets the trucks and reloads the trucks which has a time 
    complexity of O(N^2).
    This has a Big O space complexity of O(N), because of the packages that are loaded.
    """
    def run_delivery_simulation(self, provided_time, code, package_number):
        if provided_time < datetime.timedelta(hours=10, minutes=20, seconds=0):
            package_to_change = self.package_hash_table.search(9)
            package_to_change.change_delivery_address('300 State St', 'Salt Lake City', 'UT', '84103')
        else:
            print('New address for package nine has been received and updated in the system.')
        if provided_time > datetime.timedelta(hours=8, minutes=00, seconds=00):
            last_delivered_package = 'HUB'
            for package in self.truck_1.loaded_packages:
                package.set_delivery_status('Loaded in truck one')
            for package in self.truck_1.loaded_packages:
                distance = self.distance_between_nodes(last_delivered_package, self.convert_package_to_key(package))
                h, m, s = self.time_taken(distance)
                arrival_time = self.truck_1.last_delivery_time + datetime.timedelta(hours=h, minutes=m, seconds=s)
                if arrival_time < provided_time:
                    package.package_delivered(arrival_time, 'Truck One')
                    self.truck_1.update_last_delivery_time(arrival_time)
                    last_delivered_package = self.convert_package_to_key(package)
                    self.truck_1.update_miles(distance)
                else:
                    break
            distance = self.distance_between_nodes(last_delivered_package, 'HUB')
            h, m, s = self.time_taken(distance)
            arrival_time = self.truck_1.last_delivery_time + datetime.timedelta(hours=h, minutes=m, seconds=s)
            if arrival_time < provided_time:
                self.truck_1.update_last_delivery_time(arrival_time)
                self.truck_1.update_miles(distance)
                self.truck_1.update_returned_from_run()

        if provided_time > self.truck_2.departure_time:
            last_delivered_package = 'HUB'
            for package in self.truck_2.loaded_packages:
                package.set_delivery_status('Loaded in truck two')
            for package in self.truck_2.loaded_packages:
                distance = self.distance_between_nodes(last_delivered_package, self.convert_package_to_key(package))
                h, m, s = self.time_taken(distance)
                arrival_time = self.truck_2.last_delivery_time + datetime.timedelta(hours=h, minutes=m, seconds=s)
                if arrival_time < provided_time:
                    package.package_delivered(arrival_time, 'Truck Two')
                    self.truck_2.update_last_delivery_time(arrival_time)
                    last_delivered_package = self.convert_package_to_key(package)
                    self.truck_2.update_miles(distance)
                else:
                    break
            distance = self.distance_between_nodes(last_delivered_package, 'HUB')
            h, m, s = self.time_taken(distance)
            arrival_time = self.truck_2.last_delivery_time + datetime.timedelta(hours=h, minutes=m, seconds=s)
            if arrival_time < provided_time:
                self.truck_2.update_last_delivery_time(arrival_time)
                self.truck_2.update_miles(distance)
                self.truck_2.update_returned_from_run()
        if self.truck_1.returned_from_run and self.truck_2.returned_from_run:
            if self.truck_1.last_delivery_time < self.truck_2.last_delivery_time:
                if self.truck_1.last_delivery_time > self.truck_3.departure_time:
                    self.truck_3.set_departure_time(self.truck_1.last_delivery_time)
            else:
                if self.truck_2.last_delivery_time > self.truck_3.departure_time:
                    self.truck_3.set_departure_time(self.truck_2.last_delivery_time)
        elif self.truck_1.returned_from_run:
            if self.truck_1.last_delivery_time > self.truck_3.departure_time:
                self.truck_3.set_departure_time(self.truck_1.last_delivery_time)
        elif self.truck_2.returned_from_run:
            if self.truck_2.last_delivery_time > self.truck_3.departure_time:
                self.truck_3.set_departure_time(self.truck_2.last_delivery_time)
        else:
            no_departure = datetime.timedelta(hours=23, minutes=59, seconds=59)
            self.truck_3.set_departure_time(no_departure)
        if provided_time > self.truck_3.departure_time:
            last_delivered_package = 'HUB'
            for package in self.truck_3.loaded_packages:
                package.set_delivery_status('Loaded in truck three')
            for package in self.truck_3.loaded_packages:
                distance = self.distance_between_nodes(last_delivered_package, self.convert_package_to_key(package))
                h, m, s = self.time_taken(distance)
                arrival_time = self.truck_3.last_delivery_time + datetime.timedelta(hours=h, minutes=m, seconds=s)
                if arrival_time < provided_time:
                    package.package_delivered(arrival_time, 'Truck Three')
                    self.truck_3.update_last_delivery_time(arrival_time)
                    last_delivered_package = self.convert_package_to_key(package)
                    self.truck_3.update_miles(distance)
                else:
                    break
            distance = self.distance_between_nodes(last_delivered_package, 'HUB')
            h, m, s = self.time_taken(distance)
            arrival_time = self.truck_3.last_delivery_time + datetime.timedelta(hours=h, minutes=m, seconds=s)
            if arrival_time < provided_time:
                self.truck_3.update_last_delivery_time(arrival_time)
                self.truck_3.update_miles(distance)
                self.truck_3.update_returned_from_run()

        total_miles = self.truck_1.miles_driven + self.truck_2.miles_driven + self.truck_3.miles_driven

        if code == 'search':
            print('{:2>4} | {:<45} | {:<20} | {:>5} | {:>5} | {:<6} | {:<8} | {}'.format('ID', 'Address', 'City',
                                                                                         'State', 'Zip', 'weight',
                                                                                         'Deadline', 'Status'))
            print(self.package_hash_table.search(package_number))
            print('')
            print(f'Truck one miles:    {self.truck_1.miles_driven}\n'
                  f'Truck two miles:    {self.truck_2.miles_driven}\n'
                  f'Truck three miles:  {self.truck_3.miles_driven}\n'
                  f'Total miles driven: {total_miles}')

        if code == 'print all':
            self.print_all_packages()
            print('')
            print(f'Truck one miles:    {self.truck_1.miles_driven}\n'
                  f'Truck two miles:    {self.truck_2.miles_driven}\n'
                  f'Truck three miles:  {self.truck_3.miles_driven}\n'
                  f'Total miles driven: {total_miles}')

        if code == 'miles':
            print(f'Truck one miles:    {self.truck_1.miles_driven}\n'
                  f'Truck two miles:    {self.truck_2.miles_driven}\n'
                  f'Truck three miles:  {self.truck_3.miles_driven}\n'
                  f'Total miles driven: {total_miles}')

        self.truck_1.reset_truck()
        self.truck_2.reset_truck()
        self.truck_3.reset_truck()
        self.load_package_data('packages.csv')
        self.load_trucks_set_departure()
