from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from di_container import Container
from controllers import room_controller, booking_controller


def create_app() -> FastAPI:

    container = Container()
    container.config.from_yaml('config/config.yaml')
    app = FastAPI(
        title="classroom-booking",
        version="0.0.1",
    )
    container.wire(modules=[room_controller, booking_controller])
    app.container = container
    app.include_router(room_controller.router)
    app.include_router(booking_controller.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=container.config()['cors_origins'].split(','),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
