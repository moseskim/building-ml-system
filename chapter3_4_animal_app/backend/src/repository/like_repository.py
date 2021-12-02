from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from src.entities.common import Count
from src.entities.like import LikeCreate, LikeModel, LikeQuery
from src.repository.base_repository import BaseRepository

logger = getLogger(__name__)


class AbstractLikeRepository(ABC, BaseRepository):
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[LikeQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def count(
        self,
        session: Session,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        raise NotImplementedError
