from volga_it.api.transport import Transport

from ..models import Rent


def transport_history(transport: Transport):
    return (
        Rent.get_query()
        .filter(Rent.transport == transport)
        .order_by(Rent.time_start)
        .all()
    )
