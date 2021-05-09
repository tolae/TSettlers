from .Message import Message


class KeepAliveMessage(Message):
    def _parse_data(self, data):
        return 0

    def __str__(self):
        return "KeepAlive"
