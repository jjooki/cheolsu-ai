import uvicorn
import time
from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.common.config import config
from app.core.dependency import Logging
from app.core.exception import CustomException
from app.core.middleware import ResponseLoggerMiddleware
from app.router import routers
from contextlib import asynccontextmanager


def init_routers(app: FastAPI) -> None:
    print("init_routers")
    app.include_router(routers)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     from app.database.mysql.session import read_engine
#     from app.core.utils.aiohttp import SingletonAiohttp

#     SingletonAiohttp.get_aiohttp_client()
#     yield

#     # cleanup
#     await SingletonAiohttp.close_aiohttp_client()


def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_middlewares() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(ResponseLoggerMiddleware),
    ]

    return middleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="ChatBot Server",
        description="ChatBot Server API",
        version=config.RELEASE_VERSION,
        dependencies=[Depends(Logging)],
        middleware=init_middlewares(),
        # lifespan=lifespan,
    )
    init_routers(app)
    init_listeners(app)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return app


app = create_app()