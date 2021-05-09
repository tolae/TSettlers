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


class ResourceProdSet(object):
    def __init__(self, resource_prods):
        self.clay = resource_prods[0]
        self.clay_p = ResourceProdSet._calculate_probability(resource_prods[1])
        self.ore = resource_prods[2]
        self.ore_p = ResourceProdSet._calculate_probability(resource_prods[3])
        self.sheep = resource_prods[4]
        self.sheep_p = ResourceProdSet._calculate_probability(resource_prods[5])
        self.wheat = resource_prods[6]
        self.wheat_p = ResourceProdSet._calculate_probability(resource_prods[6])
        self.wood = resource_prods[7]
        self.wood_p = ResourceProdSet._calculate_probability(resource_prods[8])

    @staticmethod
    def _calculate_probability(hex_num):
        if hex_num == 2 or hex_num == 12:
            return 1 /  36
        elif hex_num == 3 or hex_num == 11:
            return 2 / 36
        elif hex_num == 4 or hex_num == 10:
            return 3 / 36
        elif hex_num == 5 or hex_num == 9:
            return 4 / 36
        elif hex_num == 6 or hex_num == 8:
            return 5 / 36
        else:
            assert False


class ResourceProductionMessage(ResourceMessage):
    def _parse_data(self, data):
        return ResourceProdSet(bytearray(data))

    def __str__(self):
        return "RES PROD - C{}|{:.2f} O{}|{} S{}|{} T{}|{} W{}|{}".format(
            self.data().clay, self.data().clay_p,
            self.data().ore, self.data().ore_p,
            self.data().sheep, self.data().sheep_p,
            self.data().wheat, self.data().wheat_p,
            self.data().wood, self.data().wood_p
        )
