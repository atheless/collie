import logging
from abc import ABC, abstractmethod

from alembic import command
from alembic.config import Config
from sqlalchemy import exc, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from security.models import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO, format='[Relational Database]: %(message)s')
logger = logging.getLogger(__name__)


class Database(ABC):
    def __init__(self, db_url, config=None):
        config = config or {}
        self.engine = create_engine(db_url, **config)
        self.Session = sessionmaker(bind=self.engine)
        # self.create_tables()
        # self.migrate_tables()

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def get_session(self):
        pass

    def _handle_error(self, e, db_type):
        logger.error(f"Error creating {db_type} tables: {e}")

    def migrate_tables(self):
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("script_location", "migration")
        alembic_cfg.set_main_option("sqlalchemy.url", str(self.engine.url))
        try:
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migration successful.")
        except SQLAlchemyError as e:
            self._handle_error(e, "migration")


class SQLiteDatabase(Database):

    def create_tables(self):
        try:
            BaseModel.metadata.create_all(self.engine)
            logger.info("SQLite tables created successfully.")
        except exc.SQLAlchemyError as e:
            self._handle_error(e, "SQLite")

    def get_session(self):
        return self.Session(autocommit=False, autoflush=True)


class PostgresSQLDatabase(Database):
    def create_tables(self):
        try:
            BaseModel.metadata.create_all(self.engine)
            logger.info("PostsgreSQL tables created successfully.")
        except exc.SQLAlchemyError as e:
            self._handle_error(e, "PostsgreSQL")

    def get_session(self):
        return self.Session(autocommit=False, autoflush=True)


