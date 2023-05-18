# Class to create 3 delivery trucks

import datetime
class Truck:

    def __init__(self, num_packages, speed, packages, current_time, mileage, departure_time, address, truck_number, weight):
        self.num_packages = num_packages
        self.speed = speed
        self.packages = list(packages)
        self.current_time = current_time
        self.mileage = mileage
        self.departure_time = departure_time
        self.address = address
        self.truck_number = truck_number
        self.weight = weight

    def __str__(self):
        return('%s, %s, %s, %s, %s, %s, %s, %s, %s'% self.num_packages, self.speed, self.packages, self.current_time,
               self.mileage, self.departure_time, self.address, self.truck_number, self.weight)






