import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship, Session

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
        transaction = Transaction(amount=amount, type=transaction_type, timestanp=datetime.datetime.now(), account=self)
        return transaction

    def deposit(self, amount):
        print(f"depos de {amount}€")
        self.balance += amount
        new_transaction = self.create_transaction(amount, "deposit")
        self.session.add(new_transaction)
        self.session.commit()
        return self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            print(f"retraint de {amount}€")
            self.balance -= amount
            new_transaction = self.create_transaction(amount, "withdrawal")
            self.session.add(new_transaction)
            self.session.commit()
            return self.balance
        else:
            return("Error: Insufficient funds")

    def get_balance(self):
        return self.balance
    
    def transfer(self, account_from, amount):
        if self.withdraw(amount):
            account_from.deposit(amount)
            return True
        else:
            return False

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    amount = Column(Float)
    type = Column(String)
    timestanp = Column(DateTime)
    account = relationship("Account", back_populates="transactions")