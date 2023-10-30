from ..models import Transport, TransportTypeFilter


def list(limit: int, offset: int, transport_type: TransportTypeFilter):
    q = Transport.get_query().limit(limit).offset(offset)
    if transport_type != "All":
        q.filter(Transport.transport_type == transport_type)
    return q.all()
