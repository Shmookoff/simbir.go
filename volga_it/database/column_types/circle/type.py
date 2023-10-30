from typing import Optional

from sqlalchemy import Dialect
from sqlalchemy.dialects.postgresql.base import PGDialect
from sqlalchemy.sql.type_api import (
    UserDefinedType,
    _BindProcessorType,
    _ResultProcessorType,
)

from .adapter.type import PostgresCircle


class Circle:
    def __init__(self, x: float, y: float, r: float) -> None:
        self.__x = x
        self.__y = y
        self.__r = r

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def r(self):
        return self.__r


class CircleType(UserDefinedType):
    cache_ok = True

    class comparator_factory(UserDefinedType.Comparator):
        def __eq__(self, other):
            return self.bool_op("~=")(other)

        def contains(self, other):
            return self.bool_op("@>")(other)

    def get_col_spec(self, **kwargs):
        return "CIRCLE"

    def bind_processor(
        self, dialect: Dialect = PGDialect()
    ) -> _BindProcessorType[Circle]:
        def process(value: Circle | None):
            if value is None:
                return None
            return PostgresCircle(((value.x, value.y), value.r))

        return process

    def result_processor(
        self, dialect: Dialect, coltype: object
    ) -> Optional[_ResultProcessorType[Circle]]:
        def process(value: PostgresCircle):
            if value is not None:
                return Circle(value[0][0], value[0][1], value[1])
            return value

        return process
