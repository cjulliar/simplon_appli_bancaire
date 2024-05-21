import pytest
import source.bank as bank
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from source.init_db import init_db
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

# db = init_db()
# Session = sessionmaker(bind=db)
# session = Session()


@pytest.fixture(scope="function")
def session():
    # Créez une mock session utilisant UnifiedAlchemyMagicMock
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()


@pytest.fixture
def account_factory(session):
    def account0(balance):
        return bank.Account(session=session(), balance=balance)
    return account0

