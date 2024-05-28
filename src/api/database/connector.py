from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
import databases
from dotenv import load_dotenv
from icecream import ic
import os

class Connector:
    database = None
    engine = None
    SessionLocal = None
    Base = None
    connector_instance = None

    def __init__(self):
        if not Connector.connector_instance:
            ic("Creating new instance")
            self._create_instance()

    @classmethod
    def get_instance(cls):
        if cls.connector_instance is None:
            cls.connector_instance = cls()
        return cls.connector_instance

    def _create_instance(self):
        load_dotenv()
        database_url = os.getenv("DATABASE_URL", None)
        ic(database_url)
        Connector.database = databases.Database(database_url)
        Connector.engine = create_engine(database_url, pool_size=20, max_overflow=50)
        Connector.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Connector.engine)
        Connector.Base = declarative_base()

        
    def get_database(self):
        return Connector.database    

    def get_engine(self):
        return Connector.engine
    
    def get_session_local(self):
        return Connector.SessionLocal
    
    def get_base(self):
        return Connector.Base
    
    def create_all(self):
        Connector.Base.metadata.create_all(bind=Connector.engine)