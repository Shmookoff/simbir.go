from volga_it.api.account import Account

from ..models import Transport
from ..schemas import AdminTransportCreate, TransportCreate


def create(owner: Account, data: TransportCreate):
    return Transport.create(**{**data.to_model_data(), "owner_id": owner.id})


def create_as_admin(data: AdminTransportCreate):
    return Transport.create(**data.to_model_data())
