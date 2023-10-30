from typing import Optional

from sqlalchemy import Dialect
from sqlalchemy.dialects.postgresql.base import PGDialect
from sqlalchemy.sql.type_api import (
    UserDefinedType,
    _BindProcessorType,
    _ResultProcessorType,
)

from .adapter.type import PostgresPoint


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class PointType(UserDefinedType):
    cache_ok = True

    class comparator_factory(UserDefinedType.Comparator):
        def __eq__(self, other):
            return self.bool_op("~=")(other)

        def contained_in(self, other):
            return self.bool_op("<@")(other)

    def get_col_spec(self, **kwargs):
        return "POINT"

    def bind_processor(
        self, dialect: Dialect = PGDialect()
    ) -> _BindProcessorType[Point]:
        def process(value: Point | None):
            if value is None:
                return None
            return PostgresPoint((value.x, value.y))

        return process

    def result_processor(
        self, dialect: Dialect, coltype: object
    ) -> Optional[_ResultProcessorType[Point]]:
        def process(value: PostgresPoint):
            if value is not None:
                return Point(value[0], value[1])
            return value

        return process
