from source.bank import Account, Transaction
import pytest
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from source.init_db import init_db

def main(session):
    account1 = Account(session, 70.0)
    account2 = Account(session, 50.0)
    session.commit()

    account1.deposit(100)
    account2.deposit(50)

    account1.transfer(account2, 50)

    print("Solde du compte 1:", account1.balance)
    print("Solde du compte 2:", account2.balance)

if __name__ == "__main__":
    db = init_db()
    Session = sessionmaker(bind=db)
    session = Session()
    main(session)