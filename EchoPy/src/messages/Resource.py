from .Message import Message


class ResourceSet(object):
    def __init__(self, resources):
        self.clay = resources[0]
        self.ore = resources[1]
        self.sheep = resources[2]
        self.wheat = resources[3]
        self.wood = resources[4]


class ResourceMessage(Message):
    def _parse_data(self, data):
        return ResourceSet(bytearray(data))

    def __getitem__(self, indices):
        arr = [self.data().clay, self.data().ore, self.data().sheep, self.data().wheat, self.data().wood]
        return arr[indices]

    def __str__(self):
        return "RESOURCES - C{} O{} S{} T{} W{}".format(
            self.data().clay, self.data().ore, self.data().sheep, self.data().wheat, self.data().wood
        )


# For self documentation
class ResourceProductionMessage(ResourceMessage):
    def __str__(self):
        return "RES PROD - C{} O{} S{} T{} W{}".format(
            self.data().clay, self.data().ore, self.data().sheep, self.data().wheat, self.data().wood
        )
