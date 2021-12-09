from abc import ABC, abstractmethod

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.middleware.logger import configure_logger
from src.schema.base import Base

logger = configure_logger(__name__)


class AbstractTableRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_table(
        self,
        engine: Engine,
        table: Base,
        checkfirst: bool = True,
    ):
        raise NotImplementedError

    @abstractmethod
    def create_index(
        engine: Engine,
        table: Base,
        column: Column,
        checkfirst: bool = True,
        unique: bool = False,
    ) -> Index:
        raise NotImplementedError
