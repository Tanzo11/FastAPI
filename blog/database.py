from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database, database_exists


url = 'postgresql://postgres:Tanzo@172.17.0.1:5433/review'


'''if not database_exists(url):
        
    create_database(url)

else:
    drop_database(url)
    create_database(url)'''

engine = create_engine(url,pool_size =50, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base=declarative_base()

def get_fastdb():
    fastdb = SessionLocal()
    try:
        yield fastdb
    finally:
        fastdb.close