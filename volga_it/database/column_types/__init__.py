from psycopg import Connection

from .circle import Circle
from .circle.adapter import register_circle
from .point import Point
from .point.adapter import register_point


def register_column_types(connection: Connection):
    register_circle(connection)
    register_point(connection)


__all__ = ("Circle", "Point", "register_column_types")
