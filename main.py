import csv
from datetime import *
import hash_table
from deliveredPackages import deliveredPackages
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
        # create list from csv file
        CSVPackages = list(CSVPackages)

        for package in CSVPackages:
            pID = int(package[0])
            address = package[1]
            city = package[2]
            zip = package[3]
            weight = package[4]
            deadline = package[5]
            status = "At Hub"

            package = Package(pID, address, city, zip, weight, deadline, status)

            package_hash_table.insert(pID, package)


def find_address(address, addressList):

    for a in addressList:
        if address == a[2]:
            return a[0]
    return address

def find_distance(x, y, _list):
    distanceList = _list
    distance = distanceList[x][y]
    if distance == '':
        distance = distanceList[y][x]

    return float(distance)

def get_truck_packages(truck, hashTable):
    truck_package_list = []
    for item in truck.packages:
        package = hashTable.find_package(item)
        truck_package_list.append(package)
    return truck_package_list


def deliver_packages(truck, hashTable, list_of_addresses, list_of_distances, delivery_list):
    # create initial list of packages on truck
    remaining_packages = []
    addressList = list_of_addresses
    distancesList = list_of_distances

    # fill remaining packages list from hash table
    for item in truck.packages:
        p = hashTable.find_package(item)
        remaining_packages.append(p)

    # create empty list for packages once delivered - this will be a list of deliveredPackages
    delivered_packages = []
    START_MILES = int(0)
    # the first package on each truck's list is the package that needs delivered first
    # obtain package and address for first deliver
    first_package = remaining_packages[0]
    truck_first_delivery_address = first_package.address
    
    # drive to first delivery, already determined
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
    delivered = deliveredPackages(first_package.id, first_package.address, first_package.deadline, first_package.city,
                                  first_package.zip, first_package.weight, first_package.status, departure_time, time,
                                  delivery_time)

    # add first package to the delivered packages list, remove from remaining packages
    delivered_packages.append(delivered)
    remaining_packages.remove(first_package)

    # begin sorting the packages using nearest neighbor algorithm
    # complexity: O(N)
    next_package_to_deliver = None
    # packages are removed after each delivery
    # loop will iterate until there are no more packages on the list
    while len(remaining_packages) > 0:
        x = int(find_address(truck.address, addressList))
        next_package_distance = 999
        for package in remaining_packages:
            if package is not None:
                y = int(find_address(package.address, addressList))
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

        package_delivered = deliveredPackages(next_package_to_deliver.id, next_package_to_deliver.address,
                                              next_package_to_deliver.deadline, next_package_to_deliver.city,
                                              next_package_to_deliver.zip, next_package_to_deliver.weight,
                                              next_package_to_deliver.status, package_departure_time, package_time,
                                              package_delivery_time)

        # add each deliveredPackage to the list, remove package from remaining packages
        delivered_packages.append(package_delivered)
        remaining_packages.remove(next_package_to_deliver)

    # all packages on truck list have been delivered, return to HUB
    x = (int(find_address(truck.address, addressList)))
    # find mileage from current location to HUB, and add miles plus travel time to truck's statistics
    mileageHome = find_distance(x, 0, distancesList)
    truck.mileage = truck.mileage + round(mileageHome)
    truck.current_time = truck.current_time + timedelta(minutes=(int(round((mileageHome / truck.speed) * 60))))
    print(len(delivered_packages))
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
                   0, datetime.timedelta(hours=8), '4001 South 700 East')

    truck2 = Truck(16, 18, [3, 18, 36, 37, 6, 25, 28, 32, 2, 33, 31, 22, 40, 4, 17, 21],
                   datetime.timedelta(hours=9, minutes=5),
                   0, datetime.timedelta(hours=9, minutes=5), '4001 South 700 East')

    truck3 = Truck(8, 18, [9, 8, 5, 38, 10, 27, 35, 7], datetime.timedelta(hours=8), 0,
                   datetime.timedelta(hours=10, minutes=30),
                   '4001 South 700 East')

    truck1_delivery_list = deliver_packages(truck1, packageHashTable, addressList, distancesList, truck1_delivery_list)
    for delivery in truck1_delivery_list:
        final_delivery_list.append(delivery)

    print('TRUCK 2:')
    truck2_delivery_list = deliver_packages(truck2, packageHashTable, addressList, distancesList, truck2_delivery_list)
    for delivery in truck2_delivery_list:
        final_delivery_list.append(delivery)

    # truck 3 can leave once the first truck has returned to home base
    if truck1.current_time < truck2.current_time:
        truck3.departure_time = truck1.current_time
    else:
        truck3.departure_time = truck2.current_time

    print('TRUCK 3:')
    truck3_delivery_list = deliver_packages(truck3, packageHashTable, addressList, distancesList, truck3_delivery_list)
    for delivery in truck3_delivery_list:
        final_delivery_list.append(delivery)

    # calculate total mileage for all 3 trucks
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage
    print(total_mileage)

    for delivery in final_delivery_list:
        print(delivery.delivery_time)

    while True:
        try:
            user_time = input('Enter time to search: HH:MM, enter \'4\' to exit\n').split()
            for time in user_time:
                hour, min = [int(i) for i in time.split(":")]
            time_to_search = timedelta(hours=hour, minutes=min)
            break;
        except ValueError:
            print('Invalid time. Please enter time in format \'HH:MM\'')
            continue

    for delivery in final_delivery_list:
        if time_to_search < delivery.departure_time:
            delivery.status = 'At Hub'
        elif delivery.departure_time <= time_to_search < delivery.delivery_time:
            delivery.status = 'En Route'
        elif time_to_search >= delivery.delivery_time:
            delivery.status = 'Delivered'


        print(delivery.__str__())
        # reset delivery status
        delivery.status = 'Delivered'


