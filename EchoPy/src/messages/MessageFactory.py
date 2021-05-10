from .Items import ItemsMessage
from .KeepAlive import KeepAliveMessage
from .Message import Message
from .Resource import ResourceMessage, ResourceProductionMessage
from .Unknown import UnknownMessage


def build(package):
    t = package['type']
    if t == Message.KEEP_ALIVE:
        return KeepAliveMessage(package)
    elif t == Message.RESOURCE_SET:
        return ResourceMessage(package)
    elif t == Message.RESOURCE_PROD:
        return ResourceProductionMessage(package)
    elif t == Message.ITEMS:
        return ItemsMessage(package)
    else:
        return UnknownMessage(package)
