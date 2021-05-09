from abc import abstractmethod, ABC


class Message(ABC):
    KEEP_ALIVE = 1
    RESOURCE_SET = 2
    RESOURCE_PROD = 3
    ITEMS = 4

    def __init__(self, package):
        self._type = package['type']
        self._length = package['length']
        self._data = self._parse_data(package['data'])

    @abstractmethod
    def _parse_data(self, data):
        pass

    def type(self):
        return self._type

    def length(self):
        return self._length

    def data(self):
        return self._data

    def __len__(self):
        return self._length
