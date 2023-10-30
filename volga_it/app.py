from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy.exc import IntegrityError

from volga_it.api.router import api_router
from volga_it.database.session import get_engine
from volga_it.exceptions.integrity_error import integrity_error_handler

app = FastAPI()

app.add_middleware(DBSessionMiddleware, custom_engine=get_engine())

app.add_exception_handler(IntegrityError, integrity_error_handler)


app.include_router(api_router)
