from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.Exceptions.domain_exceptions import DomainException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
