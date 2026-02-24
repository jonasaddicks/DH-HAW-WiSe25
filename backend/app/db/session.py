import time
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from app.logging import Source, log_error, log_info, log_warning
from app.model import Base

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', 'undefined')
MAX_RETRIES = 10
SLEEP_SECONDS = 3

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        with engine.connect() as conn:
            pass
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        log_info(Source.db_session, 'Connection to DB successful')
        break
    except OperationalError as e:
        log_warning(Source.db_session, f'Connection to DB failed - attempt {attempt}/{MAX_RETRIES}: {repr(e)}')
        time.sleep(SLEEP_SECONDS)
    except Exception as e:
        log_error(Source.db_session, f'URL: {SQLALCHEMY_DATABASE_URL} - {repr(e)}')
else:
    log_error(Source.db_session, 'Connection to DB failed')
    raise RuntimeError('Connection to DB failed')

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()