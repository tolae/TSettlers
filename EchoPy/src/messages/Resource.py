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


class ResourceHex(object):
    CLAY = 1
    ORE = 2
    SHEEP = 3
    WHEAT = 4
    WOOD = 5

    def __init__(self, hex_tile):
        self.type = hex_tile[0]
        self.prob = ResourceHex._calculate_probability(hex_tile[1])
        self.amt = hex_tile[2]

    @staticmethod
    def _calculate_probability(hex_num):
        if hex_num == 2 or hex_num == 12:
            return 1 / 36
        elif hex_num == 3 or hex_num == 11:
            return 2 / 36
        elif hex_num == 4 or hex_num == 10:
            return 3 / 36
        elif hex_num == 5 or hex_num == 9:
            return 4 / 36
        elif hex_num == 6 or hex_num == 8:
            return 5 / 36
        else:
            return 0


class ResourceProdSet(object):
    def __init__(self, hexes):
        self.amount = {
            ResourceHex.CLAY: 0, ResourceHex.ORE: 0, ResourceHex.SHEEP: 0, ResourceHex.WHEAT: 0, ResourceHex.WOOD: 0
        }
        self.scaled = {
            ResourceHex.CLAY: 0, ResourceHex.ORE: 0, ResourceHex.SHEEP: 0, ResourceHex.WHEAT: 0, ResourceHex.WOOD: 0
        }
        for hex_tile in hexes:
            self.amount[hex_tile.type] += hex_tile.amt
            self.scaled[hex_tile.type] += hex_tile.prob


class ResourceProductionMessage(ResourceMessage):
    def _parse_data(self, data):
        resource_hexes = []
        data = bytearray(data)
        for i in range(0, len(data), 3):
            resource_hexes.append(ResourceHex(data[i:i+3]))

        return ResourceProdSet(resource_hexes)

    def __str__(self):
        return "RES PROD - C{}|{:.2f} O{}|{:.2f} S{}|{:.2f} T{}|{:.2f} W{}|{:.2f}".format(
            self.data().amount[ResourceHex.CLAY], self.data().scaled[ResourceHex.CLAY],
            self.data().amount[ResourceHex.ORE], self.data().scaled[ResourceHex.ORE],
            self.data().amount[ResourceHex.SHEEP], self.data().scaled[ResourceHex.SHEEP],
            self.data().amount[ResourceHex.WHEAT], self.data().scaled[ResourceHex.WHEAT],
            self.data().amount[ResourceHex.WOOD], self.data().scaled[ResourceHex.WOOD],
        )
