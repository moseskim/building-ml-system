from logging import getLogger
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, String, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import INT
from src.middleware.database import Base
from src.repository.abstract_repository import AbstractRepository
from src.schema.table import TABLES
from src.schema.user import UserCreate, UserModel, UserQuery

logger = getLogger(__name__)


class User(Base):
    __tablename__ = TABLES.USER.value
    id = Column(
        String(32),
        primary_key=True,
    )
    handle_name = Column(
        String(128),
        nullable=False,
        unique=False,
    )
    email_address = Column(
        String(128),
        nullable=False,
        unique=True,
    )
    age = Column(
        INT,
        nullable=False,
        unique=False,
    )
    gender = Column(
        INT,
        nullable=False,
        unique=False,
    )
    deactivated = Column(
        Boolean,
        default=False,
        nullable=False,
        unique=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class UserRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.USER.value

    def select(
        self,
        session: Session,
        query: Optional[UserQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(User.id == query.id)
            if query.handle_name is not None:
                filters.append(User.handle_name == query.handle_name)
            if query.email_address is not None:
                filters.append(User.email_address == query.email_address)
            if query.age is not None:
                filters.append(User.age == query.age)
            if query.gender is not None:
                filters.append(User.gender == query.gender)
            if query.deactivated is not None:
                filters.append(User.deactivated == query.deactivated)
        results = session.query(User).filter(and_(*filters)).order_by(User.id).limit(limit).offset(offset)
        data = [UserModel(**(self.model_to_dict(d))) for d in results]
        return data

    def select_by_ids(
        self,
        session: Session,
        user_ids: List[str],
        limit=100,
        offset=0,
    ) -> List[UserModel]:
        results = session.query(User).filter(User.id.in_(user_ids)).order_by(User.id).limit(limit).offset(offset)
        data = [UserModel(**(self.model_to_dict(d))) for d in results]
        return data

    def insert(
        self,
        session: Session,
        record: UserCreate,
        commit: bool = True,
    ) -> Optional[UserModel]:
        data = User(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=UserQuery(
                    id=data.id,
                    limit=1,
                    offset=0,
                ),
            )
            return result[0]
        return None
