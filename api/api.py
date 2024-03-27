""" This module contains the FastAPI application instance and its configuration. """

from fastapi import FastAPI

from api.handlers import movie_v1


def create_app():
    """
    Creates and configures a FastAPI application instance.
    Returns:
        FastAPI: The configured FastAPI application object.
    """
    app = FastAPI(docs_url="/")
    # app.include_router(demo.router)
    app.include_router(movie_v1.router)
    return app
