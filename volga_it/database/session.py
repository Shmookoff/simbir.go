from urllib.parse import urlparse

from psycopg import connect
from sqlalchemy import URL, create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker

from volga_it.database.column_types import register_column_types
from volga_it.settings import settings


def get_url():
    url = urlparse(str(settings.DATABASE_URI))
    return URL.create(
        drivername="postgresql+psycopg",
        username=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        database=url.path[1:],
    )


__engine = None


def receive_do_connect(dialect, conn_rec, cargs, cparams):
    connection = connect(*cargs, **cparams)
    register_column_types(connection)
    return connection


def get_engine():
    global __engine

    if __engine:
        return __engine

    __engine = create_engine(get_url(), echo=True)

    event.listens_for(__engine, "do_connect")(receive_do_connect)

    return __engine


def get_session():
    engine = get_engine()
    return scoped_session(sessionmaker(bind=engine))
