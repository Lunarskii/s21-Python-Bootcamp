from sqlalchemy import create_engine, MetaData, select, Column
from sqlalchemy.orm import sessionmaker, class_mapper
from typing import Any
from contextlib import contextmanager
import inspect
import csv

from .config import *
from ..logger import logging


"""
Implementation of the 'DB' class and additional functions.
"""


class DB:
    """
    The class implements database access using the 'SQLAlchemy' module.

    :ivar session: SQLAlchemy ORM session.
    :type session: Session | None
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_url: str):
        """
        Constructor of the 'DB' class.

        :param db_url: Database URL. String form of the URL is dialect[+driver]://user:password@host/dbname[?key=value]
        :type db_url: str
        """

        if not hasattr(self, '_initialized'):
            self._initialized = True
            logging.info(f'DB: Connecting to the database "{db_url}".')
            self._engine = create_engine(db_url)
            logging.info('DB: The connection has been successfully established.')
            self._session_factory = sessionmaker(bind=self._engine)
            self.session = self._session_factory()

    def __del__(self):
        """
        Destructor of the 'DB' class.
        Closes the current session.

        :return: None
        """

        self.close()

    @contextmanager
    def session_scope(self):
        """
        Using a session in the context manager.
        """

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def add_object(self, obj: Any) -> bool:
        """
        Adds an object to the pipeline of the current session. To apply the result, it requires calling the 'commit'
        function.

        :param obj: An instance of the class inherited from SQLAlchemy.declarative_base
        :type obj: Any

        :return: True if the object was added, otherwise False
        :rtype: bool
        """

        if obj:
            self.session.add(obj)
            return True
        return False

    def del_object(self, obj: Any) -> bool:
        """
        Deletes an object from the pipeline of the current session. To apply the result, you need to call the 'commit'
        function.

        :param obj: An instance of the class inherited from SQLAlchemy.declarative_base
        :type obj: Any

        :return: True if the object was deleted, otherwise False
        :rtype: bool
        """

        if obj:
            self.session.delete(obj)
            return True
        return False

    def run_query(self, *args: Any):
        """
        Executes a query via SQLAlchemy ORM.

        :param args: query args
        :type args: Any

        :return: Results of a query executed by SQLAlchemy ORM.
        :rtype: Query
        """

        return self.session.query(*args)

    def commit(self) -> None:
        """
        Applies all inputs from the pipeline of the current session.

        :return: None
        """

        self.session.commit()

    def close(self):
        """
        Closes the current session.

        :return: None
        """

        logging.info('DB: An attempt to close the session.')
        if self.session:
            logging.info('DB: The session has been successfully completed.')
            self.session.close()

    def create_tables(self, base: Any) -> None:
        """
        Creates all tables whose models are inherited from 'base'.

        :param base: The base class from which the database models are inherited.
        :type base: Any

        :return: None
        """

        base.metadata.create_all(self._engine)

    def drop_tables(self, base: Any) -> None:
        """
        Drops all tables whose models are inherited from 'base'.

        :param base: The base class from which the database models are inherited.
        :type base: Any

        :return: None
        """

        base.metadata.drop_all(self._engine)

    def upload(self, module: Any, base: Any, csv_path: str = 'data/') -> None:
        """
        Uploads data from .csv tables to database.

        :param module: A module that contains models inherited from 'base'.
        :type module: Any

        :param base: The base class from which the database models are inherited.
        :type base: Any

        :param csv_path: The directory that contains .csv tables.
        :type csv_path: str

        :return: None
        """

        classes = inspect.getmembers(
            module,
            lambda obj: inspect.isclass(obj) and issubclass(obj, base) and obj is not base
        )
        for cls_name, cls in classes:
            fields = []
            mapper = class_mapper(cls)
            for column_property in mapper.iterate_properties:
                column = column_property.expression
                if isinstance(column, Column) and not (column.default or column.server_default or column.primary_key):
                    fields.append(column_property.key)

            with open(csv_path + cls_name + '.csv', 'r', encoding='utf-8', newline='\n') as file:
                csv_reader = csv.reader(file, quotechar='"')
                with self.session_scope() as session:
                    for row in csv_reader:
                        cls_kwargs = dict(zip(fields, row))
                        obj = cls(**cls_kwargs)
                        session.add(obj)


def create_db(db_url=None) -> DB:
    """
    Creates a database based on the arguments received, if any, otherwise from the default config.

    :param db_url: Database URL.
    :type db_url: str

    :return: Returns an instance of the 'DB' class.
    :rtype: DB
    """

    if db_url:
        return DB(db_url)
    else:
        return DB(f'{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
