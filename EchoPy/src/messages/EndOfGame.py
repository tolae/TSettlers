from .Message import Message


class EndOfGameMessage(Message):
    def _parse_data(self, data):
        data = bytearray(data)
        pos = sorted(data[1:5], reverse=True)
        return {'VP': data[0], 'Z': data[5], 'Position': pos.index(data[0]) + 1}

    def __str__(self):
        return "EOG - VP{} Z{} POS{}".format(self.data()['VP'], self.data()['Z'], self.data()['Position'])
