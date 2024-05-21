from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime
from source.bank import Base

def init_db():
    engine = create_engine('sqlite:///bank06.db')

    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    except Exception as e:
        print(f"Error: {e}")

    return engine

