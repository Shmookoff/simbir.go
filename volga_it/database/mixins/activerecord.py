from typing import Self

from fastapi_sqlalchemy import db
from sqlalchemy.sql._typing import _ColumnExpressionArgument
from sqlalchemy_mixins.inspection import InspectionMixin
from sqlalchemy_mixins.utils import classproperty


class ModelNotFoundError(ValueError):
    pass


class ActiveRecordMixin(InspectionMixin):
    __abstract__ = True

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
            else:
                raise KeyError("Attribute '{}' doesn't exist".format(name))

        return self

    def save(self, commit=True):
        """Saves the updated model to the current entity db.
        :param commit: where to commit the transaction
        """
        db.session.add(self)
        if commit:
            self._commit_or_fail()
        return self

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Create and persist a new record for the model
        :param commit: where to commit the transaction
        :param kwargs: attributes for the record
        :return: the new model instance
        """
        return cls().fill(**kwargs).save(commit=commit)

    def update(self, commit=True, **kwargs):
        """Same as :meth:`fill` method but persists changes to database.
        :param commit: where to commit the transaction
        """
        return self.fill(**kwargs).save(commit=commit)

    def delete(self, commit=True):
        """Removes the model from the current entity session and mark for deletion.
        :param commit: where to commit the transaction
        """
        db.session.delete(self)
        if commit:
            self._commit_or_fail()

    def _commit_or_fail(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    @classmethod
    def get_query(cls):
        return db.session.query(cls)

    @classmethod
    def destroy(cls, *ids: int, commit=True):
        """Delete the records with the given ids
        :type ids: list
        :param ids: primary key ids of records
        :param commit: where to commit the transaction
        """
        for pk in ids:
            obj = cls.find(pk)
            if obj:
                obj.delete(commit=commit)
        db.session.flush()

    @classmethod
    def all(cls, *whereclause: _ColumnExpressionArgument[bool]):
        return cls.get_query().where(*whereclause).all()

    @classmethod
    def first(cls, *whereclause: _ColumnExpressionArgument[bool]):
        return cls.get_query().where(*whereclause).first()

    @classmethod
    def find(cls, id_: int) -> Self | None:
        """Find record by the id
        :param id_: the primary key
        """
        return cls.get_query().get(id_)

    @classmethod
    def find_or_fail(cls, id_: int):
        # assume that query has custom get_or_fail method
        result = cls.find(id_)
        if result:
            return result
        else:
            raise ModelNotFoundError(
                "{} with id '{}' was not found".format(cls.__name__, id_)
            )
