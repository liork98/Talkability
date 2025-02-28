from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)

# Database setup
DATABASE_URL = "sqlite:///requests.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Base.metadata.create_all(engine)
