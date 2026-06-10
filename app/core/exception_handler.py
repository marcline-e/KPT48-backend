from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import PyMongoError
from fastapi.exceptions import RequestValidationError

def register_exception_handlers(app):

    # SQLAlchemy Error
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Database SQL Error",
                "detail": str(exc)
            }
        )

    # MongoDB Error
    @app.exception_handler(PyMongoError)
    async def pymongo_exception_handler(
        request: Request,
        exc: PyMongoError
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "MongoDB Error",
                "detail": str(exc)
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "Validation Error",
                "detail": exc.errors()
            }
        )

    # General Exception
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "detail": str(exc)
            }
        )
    
    # HTTP Exception
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "HTTP Exception",
                "detail": exc.detail
            }
        )