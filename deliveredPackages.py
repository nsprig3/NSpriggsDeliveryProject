# Class to search for delivered packages
class deliveredPackages:
    def __init__(self, id, address, deadline, city, zip, weight, status, departure_time, time, delivery_time):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status
        self.departure_time = departure_time
        self.time = time
        self.delivery_time = delivery_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.deadline, self.city, self.zip,
                                                           self.weight, self.departure_time, self.status, self.time,
                                                           self.delivery_time)
