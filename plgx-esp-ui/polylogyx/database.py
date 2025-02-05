# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, INET  # noqa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from polylogyx.compat import basestring
from polylogyx.extensions import db
import abc


# Alias common SQLAlchemy names
Column = db.Column
Table = db.Table
ForeignKey = db.ForeignKey
UniqueConstraint = db.UniqueConstraint
relationship = relationship
Index = db.Index


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model, object):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    def delete_by_ids(self, record_ids):
         active_records=[]
         for record_id in record_ids:
             if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),):
                 active_records.append(record_id)
         if len(active_records)==0:
            return None
         db.session.query(self).filter(self.id.in_(active_records)).delete(synchronize_session=False)
         return db.session.commit()

    @abc.abstractmethod
    def get_entity_dict(self):
        return None



# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
