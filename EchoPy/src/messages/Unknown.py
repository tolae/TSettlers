from .Message import Message


class UnknownMessage(Message):
    def _parse_data(self, data):
        self._data = 0

    def __str__(self):
        return "UNKNOWN"
