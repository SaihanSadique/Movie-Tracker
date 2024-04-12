""" This module contains the FastAPI application instance and its configuration. """

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from api.handlers import movie_v1


def create_app():
    """
    Creates and configures a FastAPI application instance.
    Returns:
        FastAPI: The configured FastAPI application object.
    """

    app = FastAPI(docs_url="/")

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    Instrumentator().instrument(app).expose(app)

    # app.include_router(demo.router)
    app.include_router(movie_v1.router)
    return app
