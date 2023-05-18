# Class to create packages to be delivered
class Package:
    def __init__(self, id, address, city, zip, weight, deadline, status, departure_time, time, delivery_time,
                 truck_number):
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.weight = weight
        self.deadline = deadline
        self.status = status
        self.departure_time = departure_time
        self.time = time
        self.delivery_time = delivery_time
        self.truck_number = truck_number

    def __str__(self):
        return "%s | %s | %s, %s, %s | %s | %s | %s | %s | %s | %s" % (
            self.time, self.id, self.address, self.city, self.zip,
            self.weight, self.deadline, self.departure_time, self.status,
            self.delivery_time, self.truck_number)


