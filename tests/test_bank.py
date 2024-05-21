# test_bank.py


import pytest
from unittest.mock import Mock
from source.example_app import main
from source.bank import Account, Transaction
from datetime import datetime


@pytest.fixture
def mock_session():
    return Mock()


def test_main(mock_session):
    main(mock_session)
    assert mock_session.add.call_count == 4 
    assert mock_session.commit.call_count == 5  

def account_factory(mock_session):
    def create_account(balance=0, account_id=None):
        account = Account(account_id=account_id, balance=balance, session=mock_session)
        mock_session.add(account)
        return account
    return create_account

def test_main(mock_session):
    main(mock_session)
    assert mock_session.add.call_count == 4
    assert mock_session.commit.call_count == 4

def test_accounts_deposit(account_factory):
    account01 = account_factory(100)
    account02 = account_factory(50)
    assert account01.get_balance() == 100
    assert account02.get_balance() == 50
    account01.deposit(100)
    account02.deposit(50)
    assert account01.get_balance() == 200
    assert account02.get_balance() == 100

def test_accounts_withdraw(account_factory, mock_session):
    account01 = account_factory(100)
    account01.withdraw(70)
    assert account01.get_balance() == 30
    transaction = account01.session.query(Transaction).first()
    assert transaction.type == "withdrawal"
    assert account01.session.commit.call_count == 1

@pytest.mark.database
def test_commit(account_factory):
    account03 = account_factory(balance=0)
    account03.deposit(2000)
    last_transaction = account03.transactions[-1]
    assert account03.get_balance() == 2000
    assert last_transaction.type == "deposit"
    assert (datetime.now() - last_transaction.timestamp).total_seconds() < 2
    assert account03.session.commit.call_count == 1


def test_accounts_transfer(account_factory, mock_session):
    account01 = account_factory(100)
    account02 = account_factory(50)
    account01.transfer(account02, 20)
    assert account01.get_balance() == 80
    assert account02.get_balance() == 70

    last_transaction_account01 = account01.transactions[-1]
    last_transaction_account02 = account02.transactions[-1]
    assert last_transaction_account01.type == "transfer_withdrawal"
    assert last_transaction_account02.type == "transfer_deposit"
    assert (datetime.now() - last_transaction_account01.timestamp).total_seconds() < 2
    assert (datetime.now() - last_transaction_account02.timestamp).total_seconds() < 2
    assert mock_session.commit.call_count == 0
