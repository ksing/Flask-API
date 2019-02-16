import os
from logging.config import dictConfig

from flask import Flask
from flask_cache import Cache
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

"""
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})
"""


app = Flask(__name__)
cache = Cache(
    app,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': os.path.join(os.path.expanduser('~'), 'Cache'),
    },
)

app.config.from_pyfile('config.py')
CORS(app)

engine = create_engine(
    app.config['SQLALCHEMY_DB_URI'],
    convert_unicode=True,
    echo=app.config['SQLALCHEMY_ECHO'],
    pool_recycle=app.config['SQLALCHEMY_POOL_RECYCLE'],
)
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
