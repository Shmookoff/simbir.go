from psycopg.adapt import Dumper

from .type import PostgresCircle


class CircleDumper(Dumper):
    oid = PostgresCircle.oid

    def dump(self, elem: PostgresCircle):
        return elem.to_string()
