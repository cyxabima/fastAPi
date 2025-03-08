from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.
# database_password}@{settings.database_host}/{settings.database_name}"

SQLALCHEMY_DATABASE_URL = settings.database_uri

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
