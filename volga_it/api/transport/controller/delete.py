from ..models import Transport


def delete(transport: Transport):
    return transport.delete()
