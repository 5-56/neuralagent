from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = ('postgresql://' + os.getenv('DB_USERNAME') + ':' + os.getenv('DB_PASSWORD') +
                '@' + os.getenv('DB_HOST') + ':' + os.getenv('DB_PORT') + '/' + os.getenv('DB_DATABASE')) \
    if not os.getenv('DB_CONNECTION_STRING') else os.getenv('DB_CONNECTION_STRING')

# Pooling and diagnostics
POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '5'))
MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '10'))
POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '1800'))  # seconds
ECHO = os.getenv('SQL_ECHO', 'false').lower() == 'true'

engine = create_engine(
    DATABASE_URL,
    echo=ECHO,
    pool_pre_ping=True,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_recycle=POOL_RECYCLE,
)

SessionLocal = sessionmaker(class_=Session, bind=engine, autocommit=False, autoflush=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
