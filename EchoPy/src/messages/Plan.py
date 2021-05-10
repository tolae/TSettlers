from .Message import Message


class PlanMessage(Message):
    def _parse_data(self, data):
        try:
            return int(data)
        except ValueError:
            pass # Input was from client, should be from server

    def __str__(self):
        return "PLAN - TO BE FILLED"
