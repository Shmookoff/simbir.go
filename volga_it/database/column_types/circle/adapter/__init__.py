from psycopg import Connection

from .dumper import CircleDumper
from .loader import CircleLoader
from .type import PostgresCircle


def register_circle(connection: Connection):
    connection.adapters.register_dumper(PostgresCircle, CircleDumper)
    connection.adapters.register_loader(PostgresCircle.oid, CircleLoader)


__all__ = ("CircleDumper", "CircleLoader", "PostgresCircle", "register_circle")
