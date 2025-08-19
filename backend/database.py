from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLite database
engine = create_engine('sqlite:///exercises.db', echo=True)

Base = declarative_base()

# Define Exercise table
class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

# Create the table
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()