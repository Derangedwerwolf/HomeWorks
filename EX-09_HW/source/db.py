import configparser
import pathlib

from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, declarative_base


Base = declarative_base()

# URI:  postgresql://username:password@domain:port/database

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
database = config.get('DEV_DB', 'DB_NAME')

URI = f"postgresql://{username}:{password}@{domain}:{port}/{database}"

engine = create_engine(URI, echo=False)
#DBSession = sessionmaker(bind=engine)
session = Session(bind=engine)