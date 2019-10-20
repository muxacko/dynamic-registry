import pytest
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from registry import Registry


@pytest.fixture
def db() -> Engine:
    return create_engine('sqlite:///:memory:', echo=True)


@pytest.fixture
def session(db: Engine) -> Session:
    return sessionmaker(bind=db)()


@pytest.fixture
def registry(db: Engine, session: Session):
    return Registry(session)
