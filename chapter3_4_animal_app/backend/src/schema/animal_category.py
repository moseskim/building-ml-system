from datetime import datetime
from typing import Optional

from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery


class AnimalCategoryQuery(AbstractQuery):
    id: Optional[str]
    name: Optional[str]
    is_deleted: Optional[bool] = False


class AnimalCategoryCreate(AbstractCreate):
    id: str
    name: str


class AnimalCategoryModel(AbstractModel):
    id: str
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
