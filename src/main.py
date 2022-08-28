from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

from admin import AdminApp
from di_container import Container


def create_app() -> FastAPI:
    """Factory that create FastAPI application.

    """

    container = Container()
    container.config.from_yaml('config/config.yaml')
    app = FastAPI(
        title="classroom-booking",
        version="0.0.1",
    )

    app.container = container
    app.add_middleware(
        CORSMiddleware,
        allow_origins=container.config()['cors_origins'].split(','),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    AdminApp(app, container.config()["db_connection_string"])
    return app


app = create_app()


@app.get("/")
async def get_root():
    return None


@app.on_event("startup")
async def startup() -> None:
    """Application startup event handler.

    """

    ...


@app.on_event("shutdown")
async def shutdown() -> None:
    """Application shutdown event handler.

    """

    ...


@app.exception_handler(StarletteHTTPException)
async def http_errors_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    """HTTP errors handler.

    Parameters
    ----------
    `request` : `Request`
        Incoming HTTP request object.
    `exc` : `StarletteHTTPException`
        HTTP exception object.

    Return
    ------
    `JSONResponse`
        Error details in JSON format {"detail": "some message"}

    """

    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def internal_errors_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Internal errors handler.

    Parameters
    ----------
    `request` : `Request`
        Incoming HTTP request object.
    `exc` : `Exception`
        Exception object.

    Return
    ------
    `JSONResponse`
        Error details in JSON format {"detail": "some message"}

    """

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
