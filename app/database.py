from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import create_database, database_exists
from urllib.parse import quote_plus
from .config import settings


SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' % quote_plus (settings.database_password))


engine = create_engine(SQLALCHEMY_DATABASE_URL)


# if not database_exists(engine.url):
#     create_database(engine.url)


SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
