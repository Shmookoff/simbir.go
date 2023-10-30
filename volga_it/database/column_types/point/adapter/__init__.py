from psycopg import Connection

from .dumper import PointDumper
from .loader import PointLoader
from .type import PostgresPoint


def register_point(connection: Connection):
    connection.adapters.register_dumper(PostgresPoint, PointDumper)
    connection.adapters.register_loader(PostgresPoint.oid, PointLoader)


__all__ = ("PointDumper", "PointLoader", "PostgresPoint", "register_point")
