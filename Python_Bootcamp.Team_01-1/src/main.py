import logging
import asyncio
import argparse

from main_package.bot.controller import Controller
from main_package.db_service import models
from main_package.db_service.base import Base
from main_package.db_service.db import create_db
from main_package.logger import logger


def load_db():
    db = create_db()
    db.create_tables(Base)
    db.upload(models, Base)


def clear_db():
    db = create_db()
    db.drop_tables(Base)


def run_bot():
    from main_package.bot import run
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run.main())
    Controller().__del__()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_bot', action='store_true', help='Run bot.')
    parser.add_argument('--load_db', action='store_true', help='Load all default data to the database.')
    parser.add_argument('--clear_db', action='store_true', help='Deletes all created tables in the database.')
    parser.add_argument('--debug', action='store_true', help='Enables logging.')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.clear_db:
        clear_db()
    if args.load_db:
        load_db()
    if args.run_bot:
        run_bot()
