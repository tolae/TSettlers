from .Message import Message


class ItemData:
    def __init__(self, data):
        self.longest_road_length = data[0]
        self.settlements = data[1]
        self.cities = data[2]
        self.knights_used = data[3]


class ItemMessage(Message):
    def _parse_data(self, data):
        return ItemData(bytearray(data))

    def __str__(self):
        return "ITEMS - L{} S{} C{} K{}".format(
            self.data().longest_road_length, self.data().settlements, self.data().cities, self.data().knights_used
        )
