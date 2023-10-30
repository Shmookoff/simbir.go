from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from volga_it.database.column_types.circle.type import Circle, CircleType
from volga_it.database.column_types.point.type import Point, PointType

from .mixins.activerecord import ActiveRecordMixin


class BaseModel(DeclarativeBase, ActiveRecordMixin):
    __abstract__ = True
    type_annotation_map = {
        Point: PointType,
        Circle: CircleType,
    }

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
