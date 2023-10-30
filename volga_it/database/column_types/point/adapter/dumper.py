from psycopg.adapt import Dumper

from .type import PostgresPoint


class PointDumper(Dumper):
    oid = PostgresPoint.oid

    def dump(self, elem: PostgresPoint):
        return elem.to_string()
