from fastapi import Request, status
from fastapi.responses import JSONResponse
from psycopg.errors import ForeignKeyViolation
from psycopg.errors import IntegrityError as PsycopgIntegrityError
from psycopg.errors import UniqueViolation
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from volga_it.database.session import get_engine


async def integrity_error_handler(request: Request, exc: IntegrityError):
    if isinstance(exc.orig, UniqueViolation):
        table_name = exc.orig.diag.table_name
        constraint_name = exc.orig.diag.constraint_name
        # Inspect DB to get constraint object
        inspector = inspect(get_engine())
        if not table_name:
            unique_constraints = []
        else:
            unique_constraints = inspector.get_unique_constraints(table_name)
        constraint = next(c for c in unique_constraints if c["name"] == constraint_name)
        # Get column names from object
        column_names = constraint["column_names"]

        col_msg = (
            f"Column {column_names[0]}"
            if len(column_names) == 1
            else f'Combination of {", ".join(column_names)}'
        )

        return JSONResponse(
            f"{col_msg} must be unique",
            status_code=status.HTTP_409_CONFLICT,
        )
    if isinstance(exc.orig, ForeignKeyViolation):
        return JSONResponse(
            "Linked entity was not found",
            status_code=status.HTTP_409_CONFLICT,
        )

    raise exc
