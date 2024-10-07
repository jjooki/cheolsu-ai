from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class Timestamp:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            onupdate=func.now(),
            nullable=True,
        )
