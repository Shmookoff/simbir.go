from typing import Self

from psycopg import adapters

X = float
Y = float
R = float


class PostgresCircle(tuple[tuple[X, Y], R]):
    oid = adapters.types["circle"].oid

    def __new__(cls, __iterable: tuple[tuple[X, Y], R]) -> Self:
        return super().__new__(cls, __iterable)

    @classmethod
    def from_string(cls, v: str):
        point, r = v[1:-1].split(",")
        x, y = point[1:-1].split(",")
        return cls(((float(x), float(y)), float(r)))

    def to_string(self):
        return f"<({self[0][0]},{self[0][1]}),{self[1]}>"
