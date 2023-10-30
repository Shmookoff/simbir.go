from ..models import Transport
from ..schemas import AdminTransportUpdate, TransportUpdate


def update(transport: Transport, data: TransportUpdate | AdminTransportUpdate):
    transport.update(**data.to_model_data())
