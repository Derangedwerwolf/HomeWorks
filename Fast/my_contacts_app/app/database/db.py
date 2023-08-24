import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# file_config = pathlib.Path(__file__).parent.parent.joinpath("conf/config.ini")
# config = configparser.ConfigParser()
# config.read(file_config)

# username = config.get("DEV", "USER")
# password = config.get("DEV", "PASSWORD")
# domain = config.get("DEV", "DOMAIN")
# port = config.get("DEV", "PORT")
# db_name = config.get("DEV", "DB_NAME")

# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{db_name}"
# )

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, max_overflow=5)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
