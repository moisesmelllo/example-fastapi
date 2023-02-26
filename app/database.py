from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# 'postgresql://<username>:<password>@ip-address/hostname>/<database_name>' - model

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# connection to our database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:  # conectando com o servidor diretamente por SQL ao invés de usar SQLALQUEMY
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='euevoluiomegamente10', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection was succesfull!')
#         break
#     except Exception as error:
#         print('connecting to the database failed')
#         print(f'ERROR = {error}')
#         print(sleep(2))

