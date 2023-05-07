# Class to create 3 delivery trucks

import datetime
class Truck:

    def __init__(self, num_packages, speed, packages, current_time, mileage, departure_time, address):
        self.num_packages = num_packages
        self.speed = speed
        self.packages = list(packages)
        self.current_time = current_time
        self.mileage = mileage
        self.departure_time = departure_time
        self.address = address






