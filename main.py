# Nicholas Staley, Student id number: 001407981
# Package Delivery System
"""
The total time complexity for the whole program is O(N^2), because that is the highest time complexity for any of the
called methods.
The total space complexity is O(N^2), because that is achieved in the adjacency matrix with N being the addresses
served, the space complexity for the package hash table is O(N) with n being the packages.
"""
import LoadingAndDelivery
import datetime

user_entry = ''
program_1 = LoadingAndDelivery.LoadingAndDelivery('packages.csv', 'distances.csv')

"""
This allows the user to select what they wish to have happen, entered the requested information, and then begins the 
simulation in the Loading And Delivery class.
"""
while user_entry != 'exit':
    print(f'Welcome to the WGUPS System, enter the number for the operation you wish to choose:')
    print(f'1: view single package details.')
    print(f'2: view all package details.')
    print(f'3: view total miles driven.')
    print(f'4: exit program.')
    user_entry = input('Which number option would you like to choose? ')
    package_number = -1

    if user_entry == '1':
        package_number = int(input('What package number would you like to look up? '))
        time_input = input('What time in military time would you like to view HH:MM:SS? ').split(':')
        h = int(time_input[0])
        m = int(time_input[1])
        s = int(time_input[2])
        user_time = datetime.timedelta(hours=h, minutes=m, seconds=s)
        program_1.run_delivery_simulation(user_time, 'search', package_number)
        print('')
        continue_input = input('Would you like to continue? 1 to continue, 2 to exit: ')
        if continue_input == '1':
            continue
        if continue_input == '2':
            user_entry = 'exit'
        else:
            continue

    if user_entry == '2':
        time_input = input('What time in military time would you like to view HH:MM:SS? ').split(':')
        h = int(time_input[0])
        m = int(time_input[1])
        s = int(time_input[2])
        user_time = datetime.timedelta(hours=h, minutes=m, seconds=s)
        program_1.run_delivery_simulation(user_time, 'print all', package_number)
        print('')
        continue_input = input('Would you like to continue? 1 to continue, 2 to exit: ')
        if continue_input == '1':
            continue
        if continue_input == '2':
            user_entry = 'exit'
        else:
            continue

    if user_entry == '3':
        time_input = input('What time in military time would you like to view HH:MM:SS? ').split(':')
        h = int(time_input[0])
        m = int(time_input[1])
        s = int(time_input[2])
        user_time = datetime.timedelta(hours=h, minutes=m, seconds=s)
        program_1.run_delivery_simulation(user_time, 'miles', package_number)
        print('')
        continue_input = input('Would you like to continue? 1 to continue, 2 to exit: ')
        if continue_input == '1':
            continue
        if continue_input == '2':
            user_entry = 'exit'
        else:
            continue

    if user_entry == '4':
        user_entry = 'exit'

    else:
        continue
