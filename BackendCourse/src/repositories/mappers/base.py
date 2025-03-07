from typing import TypeVar

from pydantic import BaseModel

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, orm_data):
        return cls.schema.model_validate(orm_data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, schema_data):
        return cls.db_model(**schema_data.model_dump())
