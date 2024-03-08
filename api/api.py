from fastapi import FastAPI

from api.handlers import demo


def create_app():
    app = FastAPI()
    app.include_router(demo.router)
    return app
     