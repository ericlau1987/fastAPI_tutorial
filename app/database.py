from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import time
# import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

username = settings.database_username
password = settings.database_password
hostname = settings.database_hostname
port = settings.database_port
database_name = settings.database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='Bbfhansen2266728!', 
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection is successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)