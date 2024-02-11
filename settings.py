"""
Global settings for an application.
"""
import logging

from jinja2 import Environment, FileSystemLoader

from database.relational_dbs import SQLiteDatabase

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database
DATABASE_URL = 'sqlite:///sqlite_database.db'  # Postgres: 'postgresql://username:password@localhost:5432/postgres_database'
rdatabase = SQLiteDatabase(db_url=DATABASE_URL, config={})

# Migrations
EXCLUDE_TABLES_MIGRATIONS = ['users', 'sessions', 'csrf_tokens']

# CORS headers configuration
ACCESS_CONTROL_ALLOW_ORIGIN = ['http://localhost:3000']  # Adjust this to only allow specific origins

# Templates
templates = Environment(
    loader=FileSystemLoader('templates'))  # Assuming your templates are in a folder named "templates"

# Secret
SECRET = 'a5bec250c731a7b036c13548f506dbee34baf789e43c6339172584e8c14f84aa'

# Debug
DEBUG = True


PROCESS_POOL_SIZE = 4
THREAD_POO_SIZE = 4