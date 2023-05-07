# Class to create packages to be delivered
class Package:
    def __init__(self, id, address, deadline, city, zip, weight, status):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.deadline, self.city, self.zip,
                                               self.weight, self.status)


