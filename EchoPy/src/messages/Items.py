from .Message import Message


class ItemsData:
    def __init__(self, data):
        self.player = data[0]
        self.longest_road_length = data[1]
        self.knights_used = data[2]


class ItemsMessage(Message):
    def _parse_data(self, data):
        return ItemsData(bytearray(data))

    def __str__(self):
        return "ITEMS FOR P|{}[{}] - L{} K{}".format(
            "TBot" if self.data().player == 255 else "Opponent", self.data().player,
            self.data().longest_road_length, self.data().knights_used
        )
