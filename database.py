from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

engine = create_engine('postgresql://postgres:rohan752004@localhost:5432/Pizza_Project', echo = True )

Session = sessionmaker()