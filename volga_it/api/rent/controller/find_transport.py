from sqlalchemy.sql._typing import _ColumnExpressionArgument

from volga_it.api.transport import Transport, TransportTypeFilter
from volga_it.database.column_types import Circle


def find_transport(
    latitude: float, longitude: float, radius: float, type: TransportTypeFilter
):
    clauses: list[_ColumnExpressionArgument[bool]] = [
        Transport.location.contained_in(Circle(latitude, longitude, radius))
    ]
    if type != "All":
        clauses.append(Transport.transport_type == type)

    return Transport.get_query().filter(*clauses).all()
