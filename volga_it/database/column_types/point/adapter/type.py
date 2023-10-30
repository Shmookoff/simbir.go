from typing import Self

from psycopg import adapters

X = float
Y = float


class PostgresPoint(tuple[X, Y]):
    oid = adapters.types["point"].oid

    def __new__(cls, __iterable: tuple[X, Y]) -> Self:
        return super().__new__(cls, __iterable)

    @classmethod
    def from_string(cls, v: str):
        x, y = v[1:-1].split(",")
        return cls((float(x), float(y)))

    def to_string(self):
        return f"({self[0]},{self[1]})"
