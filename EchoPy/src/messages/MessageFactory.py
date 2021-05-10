from .Items import ItemsMessage
from .KeepAlive import KeepAliveMessage
from .EndOfGame import EndOfGameMessage
from .Resource import ResourceMessage, ResourceProductionMessage
from .Unknown import UnknownMessage

KEEP_ALIVE = 1
RESOURCE_SET = 2
RESOURCE_PROD = 3
ITEMS = 4
END_OF_GAME = 5


def build(package):
    t = package['type']
    if t == KEEP_ALIVE:
        return KeepAliveMessage(package)
    elif t == RESOURCE_SET:
        return ResourceMessage(package)
    elif t == RESOURCE_PROD:
        return ResourceProductionMessage(package)
    elif t == ITEMS:
        return ItemsMessage(package)
    elif t == END_OF_GAME:
        return EndOfGameMessage(package)
    else:
        return UnknownMessage(package)
