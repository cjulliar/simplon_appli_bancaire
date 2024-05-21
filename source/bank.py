import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, scoped_session, Session

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)
    transactions = relationship("Transaction", back_populates="account")

    def __init__(self, session, balance):
        self.session = session
        self.balance = balance
    
    def create_transaction(self, amount, transaction_type):
        transaction = Transaction(amount=amount, type=transaction_type, timestamp=datetime.datetime.now(), account=self)
        return transaction

    def deposit(self, amount):
        print(f"deposit de {amount}€")
        self.balance += amount
        new_transaction = self.create_transaction(amount, "deposit")
        self.session.add(new_transaction)
        self.session.commit()
        return self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            print(f"withdraw de {amount}€")
            self.balance -= amount
            new_transaction = self.create_transaction(amount, "withdrawal")
            self.session.add(new_transaction)
            self.session.commit()
            return self.balance
        else:
            raise ValueError("Error: Insufficient funds")

    def get_balance(self):
        return self.balance
    
    def transfer(self, account_to, amount):
        if self.balance < amount:
            raise ValueError("Error: Insufficient funds")

        # Perform the withdrawal from the current account
        self.balance -= amount
        withdrawal_transaction = self.create_transaction(amount, "transfer_withdrawal")
        self.session.add(withdrawal_transaction)
        
        # Perform the deposit to the target account
        account_to.balance += amount
        deposit_transaction = account_to.create_transaction(amount, "transfer_deposit")
        self.session.add(deposit_transaction)
        
        # Commit both transactions together
        self.session.commit()
        return True

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    amount = Column(Float)
    type = Column(String)
    timestamp = Column(DateTime)
    account = relationship("Account", back_populates="transactions")
