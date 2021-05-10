from .Message import Message


class PossibilitiesData(object):
    def __init__(self, data):
        self.roads = data[0]
        self.settlements = data[1]
        self.cities = data[2]
        self.dev_cards = data[3]


class PossibilitiesMessage(Message):
    def _parse_data(self, data):
        return PossibilitiesData(data)

    def __str__(self):
        return "Possibilities: R{} S{} C{} D{}".format(
            self.data().roads,
            self.data().settlements,
            self.data().cities,
            self.data().dev_cards,
        )