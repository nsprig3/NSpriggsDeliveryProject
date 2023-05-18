# Natasha Spriggs 008493354
import csv
from datetime import *
from hash_table import *
from truck import *
from package import *


# Read CSV distances file, create a list of all distances
def loadDistanceData():
    with open("DistanceTable.csv", "r") as csvDistanceFile:
        _list = []
        dataList = csv.reader(csvDistanceFile)
        for r in dataList:
            _list.append(r)
    return _list


def loadAddressData():
    with open("CSVAddresses.csv") as addresses:
        _list = []
        address_list = csv.reader(addresses)
        for a in address_list:
            _list.append(a)
    return _list


# Read CSV package file
# create a Package instance for each package in the list
def loadPackageData(filename, package_hash_table):
    with open(filename, "r") as csvPackageFile:
        CSVPackages = csv.reader(csvPackageFile)
        # skip header
        next(CSVPackages)
        # create package objects from csv file
        CSVPackages = list(CSVPackages)

        for package in CSVPackages:
            pID = int(package[0])
            address = package[1]
            city = package[2]
            zip = package[3]
            weight = package[4]
            deadline = package[5]
            status = "At Hub"
            departure_time = timedelta(hours=8, minutes = 0)
            time = timedelta(hours=8, minutes = 0)
            delivery_time = timedelta(hours=8, minutes = 0)
            truck_number = '0'
            package = Package(pID, address, city, zip, weight, deadline, status, departure_time, time, delivery_time,
                              truck_number)
            # add each package to the hash table
            package_hash_table.insert(pID, package)


# Parses the address list created from the CSV file and compares selected address to the third row in the list
# If the address is found, the a[0] is returned which is the index for the row
def find_address(address, addressList):
    for a in addressList:
        if address == a[2]:
            return a[0]
    return address


# receives two indexes and returns the distance from the two-dimensional distance table
# if the box is blank, the method will swap the indexes and return distance as a float value
def find_distance(x, y, _list):
    distanceList = _list
    distance = distanceList[x][y]
    if distance == '':
        distance = distanceList[y][x]

    return float(distance)


# receives an hour and min from user input to update the statuses in the delivery list based on the user's selection and
# the delivery and departure of the package, returns the package. Constant complexity - compares 3 values and updates
def search_time_one_package(hour, min, delivery):
    if timedelta(hours=hour, minutes=min) < delivery.departure_time:
        delivery.status = 'At Hub'
        delivery.time = timedelta(hours=hour, minutes=min)
    elif delivery.departure_time <= timedelta(hours=hour, minutes=min) < delivery.delivery_time:
        delivery.status = 'En Route'
        delivery.time = timedelta(hours=hour, minutes=min)
    elif timedelta(hours=hour, minutes=min) >= delivery.delivery_time:
        delivery.status = 'Delivered'
        delivery.time = timedelta(hours=hour, minutes=min)
    return delivery

# the address for package 9 is incorrect until 10:20AM. The correct address is stored in the address list
# changes the address for package 9 back to the incorrect address if the user selects a time before 10:20
def correct_address(hour, min, deliveryList):
    for delivery in deliveryList:
        if delivery.id == 9:
            if timedelta(hours=hour, minutes=min) < timedelta(hours=10, minutes=20):
                delivery.address = '300 State St'
                delivery.zip = '84103'

# receives an hour and minute from user input and compares that time to the departure and delivery of each package
# in the delivery list to update the status. Returns entire delivery list. O(N) complexity - must compare each delivery
def search_time_all_packages(hour, min, deliveryList):
    for delivery in deliveryList:
        if timedelta(hours=hour, minutes=min) < delivery.departure_time:
            delivery.status = 'At Hub'
            delivery.time = timedelta(hours=hour, minutes=min)
        elif delivery.departure_time <= timedelta(hours=hour, minutes=min) < delivery.delivery_time:
            delivery.status = 'En Route'
            delivery.time = timedelta(hours=hour, minutes=min)
        elif timedelta(hours=hour, minutes=min) >= delivery.delivery_time:
            delivery.status = 'Delivered'
            delivery.time = timedelta(hours=hour, minutes=min)
    return deliveryList

# receives the list of package IDs manually loaded onto the truck, searches the hash table for each package and fills
# truck package list . O(N) complexity because it must search for each item on the list
def get_truck_packages(truck, hashTable):
    truck_package_list = []
    for item in truck.packages:
        package = hashTable.find_package(item)
        truck_package_list.append(package)
    return truck_package_list

# resets the statuses and times for each package after each user selection is completed. O(N) complexity - updates each
# package on the list

def reset_lists(_list):
    for delivery in _list:
        delivery.status = 'Delivered'
        delivery.time = timedelta(hours=8)
        if delivery.id == 9:
            delivery.address = '410 S State St'
            delivery.zip = '84111'
    return _list

# primary function with the nearest neighbor algorithm to build list of deliveries based on proximity to the location
# of the truck/previous delivery.
def deliver_packages(truck, hashTable, list_of_addresses, list_of_distances):
    # create initial list of packages on truck
    remaining_packages = []
    addressList = list_of_addresses
    distancesList = list_of_distances

    # fill remaining packages list from hash table
    for item in truck.packages:
        p = hashTable.find_package(item)
        remaining_packages.append(p)

    # create empty list for packages once delivered
    delivered_packages = []
    # start each truck at 0 mileage
    START_MILES = int(0)
    '''
    for package in remaining_packages:
        truck.weight += int(package.weight)
    print(truck.weight)
    '''
    # the first package on each truck's list is the package that needs delivered first
    # obtain package and address for first delivery
    first_package = remaining_packages[0]
    truck_first_delivery_address = first_package.address

    # drive to first delivery
    x = int((find_address(truck.address, addressList)))
    y = int((find_address(truck_first_delivery_address, addressList)))

    # calculate the number of miles from the start location to the first delivery
    # add this to truck's mileage
    miles_to_next = find_distance(x, y, distancesList)
    truck.mileage = START_MILES + miles_to_next

    # calculate the time it will take to drive to first delivery based on the speed of the truck and distance
    # from hub to first delivery
    truck.current_time = truck.departure_time + timedelta(minutes=(int(round((miles_to_next / truck.speed) * 60))))

    # create times for user to search in UI
    delivery_time = truck.current_time
    time = truck.current_time
    departure_time = truck.departure_time
    first_package.status = 'Delivered'
    truck.address = first_package.address

    delivered = Package(first_package.id, first_package.address, first_package.city,
                                  first_package.zip, first_package.weight, first_package.deadline,
                                  first_package.status, departure_time, time, delivery_time, truck.truck_number)

    # add first package to the delivered packages list, remove from remaining packages
    delivered_packages.append(delivered)
    remaining_packages.remove(first_package)

    # begin looping through and sorting the packages using nearest neighbor algorithm
    # complexity: O(N) -
    next_package_to_deliver = None
    # packages are removed after each delivery
    # loop will iterate until there are no more packages on the list
    while len(remaining_packages) > 0:
        # determine x, the location of the truck
        x = int(find_address(truck.address, addressList))
        next_package_distance = 999
        for package in remaining_packages:
            if package is not None:
                # determine y, the location of each package left to be delivered
                y = int(find_address(package.address, addressList))
            # calculate the distance between each package to be delivered and the truck's current location.
            # finds the package with the shortest distance and adds it as truck's next package to deliver
            package_distance = find_distance(x, y, distancesList)
            if package_distance <= next_package_distance:
                next_package_to_deliver = package
                next_package_distance = package_distance

        miles_to_next = next_package_distance
        # drive to nearest neighboring package
        truck.mileage = truck.mileage + miles_to_next
        # determine time package will be delivered based on distance from previous package and truck speed
        truck.current_time = truck.current_time + timedelta(minutes=(int(round((miles_to_next / truck.speed) * 60))))
        # collect delivery time and departure time from truck for deliveredPackages object
        package_delivery_time = truck.current_time
        package_time = truck.current_time
        package_departure_time = truck.departure_time
        next_package_to_deliver.status = 'Delivered'
        truck.address = next_package_to_deliver.address

        package_delivered = Package(next_package_to_deliver.id, next_package_to_deliver.address,
                                              next_package_to_deliver.city, next_package_to_deliver.zip,
                                              next_package_to_deliver.weight, next_package_to_deliver.deadline,
                                              next_package_to_deliver.status, package_departure_time, package_time,
                                              package_delivery_time, truck.truck_number)

        # add each deliveredPackage to the list, remove package from remaining packages
        delivered_packages.append(package_delivered)
        remaining_packages.remove(next_package_to_deliver)

    # all packages on truck list have been delivered, return to HUB
    x = (int(find_address(truck.address, addressList)))
    # find mileage from current location to HUB, and add miles plus travel time to truck's statistics
    mileageHome = find_distance(x, 0, distancesList)
    truck.mileage = truck.mileage + round(mileageHome)
    truck.current_time = truck.current_time + timedelta(minutes=(int(round((mileageHome / truck.speed) * 60))))
    return delivered_packages


class Main:
    packageHashTable = ChainingHashTable()
    distancesList = []
    addressList = []

    loadPackageData("CSVPackages.csv", packageHashTable)
    distancesList = loadDistanceData()
    addressList = loadAddressData()
    truck1_delivery_list = []
    truck2_delivery_list = []
    truck3_delivery_list = []

    final_delivery_list = []

    # create instances for truck 1 and truck 2
    truck1 = Truck(16, 18, [15, 14, 16, 20, 19, 13, 29, 30, 34, 12, 23, 11, 26, 24, 39, 1], datetime.timedelta(hours=8),
                   0, datetime.timedelta(hours=8), '4001 South 700 East', 1, 0)

    truck2 = Truck(16, 18, [3, 18, 36, 37, 6, 25, 28, 32, 2, 33, 31, 22, 40, 4, 17, 21],
                   datetime.timedelta(hours=9, minutes=5),
                   0, datetime.timedelta(hours=9, minutes=5), '4001 South 700 East', 2, 0)

    truck3 = Truck(8, 18, [9, 8, 5, 38, 10, 27, 35, 7], datetime.timedelta(hours=8), 0,
                   datetime.timedelta(hours=10, minutes=30),
                   '4001 South 700 East', 3, 0)

    truck1_delivery_list = deliver_packages(truck1, packageHashTable, addressList, distancesList)
    for delivery in truck1_delivery_list:
        final_delivery_list.append(delivery)

    truck2_delivery_list = deliver_packages(truck2, packageHashTable, addressList, distancesList)
    for delivery in truck2_delivery_list:
        final_delivery_list.append(delivery)

    # truck 3 can leave once the first truck has returned to home base
    if truck1.current_time < truck2.current_time:
        truck3.departure_time = truck1.current_time
    else:
        truck3.departure_time = truck2.current_time

    truck3_delivery_list = deliver_packages(truck3, packageHashTable, addressList, distancesList)
    for delivery in truck3_delivery_list:
        final_delivery_list.append(delivery)

    # calculate total mileage for all 3 trucks
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage

    # USER INTERFACE
    while True:
        print()
        print('*' * 70)
        print('\t\t\t\tWGU UPS Delivery Service MAIN MENU')
        print('\t\t\t\t\t Select from the following:')
        print('*' * 70)
        print('To see the status of one package at a selected time, type \"1\"')
        print('To see the status of all packages at a selected time, type \"2\"')
        print('To view a delivery report of all packages, type \"3\"')
        print('To Exit, type \"4\"')
        print('*' * 70)

        reset_lists(final_delivery_list)

        user_selection = input('Enter Selection:\n')
        try:
            if user_selection == '4':

                print("Thank you for using WGU UPS Services! Goodbye")
                exit(0)
            elif user_selection == '1':
                while True:
                    try:
                        user_time = input('Enter time to search: HH:MM\n').split()
                        for time in user_time:
                            hour, min = [int(i) for i in time.split(":")]
                        time_to_search = timedelta(hours=hour, minutes=min)
                        correct_address(hour, min, final_delivery_list)
                        break;
                    except ValueError:
                        print('Invalid time. Please enter time in format \'HH:MM\'\n')
                        continue
                while True:
                    try:
                        user_package_ID = int(input('Enter package ID:\n'))
                        for delivery in final_delivery_list:
                            if delivery.id == user_package_ID:
                                validPID = True
                                search_time_one_package(hour, min, delivery)
                                print('=' * 70 + '\n\t\t\t\t\t\tPackage Status at '+ str(user_time))
                                print('=' * 70)

                                if delivery.status == 'Delivered':
                                    print('{} |{} | {}, {}, {} | {} | {} | {} | Delivered at {} by Truck # {}'.format(
                                        delivery.time, delivery.id, delivery.address, delivery.city, delivery.zip,
                                        delivery.weight, delivery.deadline, delivery.departure_time,
                                        delivery.delivery_time, delivery.truck_number))
                                else:
                                    print(
                                        '{}  | {} | {}, {}, {}    | {} |   {}  |  {} | {}, Expected delivery at {} by Truck # {}'.format(
                                            delivery.time, delivery.id, delivery.address, delivery.city, delivery.zip,
                                            delivery.weight, delivery.deadline, delivery.departure_time,
                                            delivery.status,
                                            delivery.delivery_time, delivery.truck_number))
                                break
                            else:
                                validPID = False
                        if validPID is False:
                            print('Package ID not found.\n')
                            continue
                        break;
                    except ValueError:
                        print('Please enter numerical package ID to search\n')

            elif user_selection == '2':
                while True:
                    try:
                        user_time = input('Enter time to search: HH:MM\n').split()
                        for time in user_time:
                            hour, min = [int(i) for i in time.split(":")]
                        time_to_search = timedelta(hours=hour, minutes=min)
                        correct_address(hour, min, final_delivery_list)
                        print('=' * 70 + '\n\t\t\t\t\t All Package Status at ' + str(user_time))
                        print('=' * 70)
                        all_packages_at_time = search_time_all_packages(hour, min, final_delivery_list)
                        for delivery in all_packages_at_time:
                            print(delivery)
                        break;
                    except ValueError:
                        print('Invalid time. Please enter time in format \'HH:MM\'\n')
                        continue
            elif user_selection == '3':
                print('=' * 25 + 'DELIVERY REPORT:' + '=' * 25)

                for delivery in final_delivery_list:
                    delivery.time = delivery.delivery_time
                    print(delivery)
                print('-' * 10)
                print('MILEAGE  Truck 1: ' + str(round(truck1.mileage, 2)) + ' Truck 2: ' + str(round(truck2.mileage, 2)) + '  Truck 3: '
                      + str(round(truck3.mileage, 2)) + ' TOTAL: ' + str(total_mileage))
                print('End of Day: ' + str(truck3.current_time))
            else:
                print('Invalid input. Please enter selection \'1-3\' or \'4\' to Exit\n')
        except ValueError:
            print('Invalid entry. Please enter numerical selection \'1-3\' or \'4\' to Exit\n')
