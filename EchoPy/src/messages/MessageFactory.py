import struct

from .Items import ItemsMessage
from .KeepAlive import KeepAliveMessage
from .EndOfGame import EndOfGameMessage
from .Plan import PlanMessage
from .Possiblities import PossibilitiesMessage
from .Resource import ResourceMessage, ResourceProductionMessage
from .Unknown import UnknownMessage

UNKNOWN = 0
KEEP_ALIVE = 1
RESOURCE_SET = 2
RESOURCE_PROD = 3
ITEMS = 4
END_OF_GAME = 5
PLAN = 6
POSSIBILITIES = 7


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
    elif t == PLAN:
        return PlanMessage(package)
    elif t == POSSIBILITIES:
        return PossibilitiesMessage(package)
    else:
        return UnknownMessage(package)


def to_bytearray(msg):
    header = struct.pack('>HB', msg.length(), msg.type())
    if msg.type() == PLAN:
        return bytearray(header + struct.pack('B', msg.data()))
    return None
