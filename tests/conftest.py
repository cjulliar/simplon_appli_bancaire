import pytest
import source.bank as bank
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from source.init_db import init_db

db = init_db()
Session = sessionmaker(bind=db)
session = Session()

@pytest.fixture
def account01():
    return bank.Account(session, 100)


@pytest.fixture
def account02():
    return bank.Account(session, 50)