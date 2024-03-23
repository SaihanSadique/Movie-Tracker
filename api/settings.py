"""Settings for the API."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the API."""

    mongo_connection_string: str = Field(
        "mongodb://movietracker_dbAdmin:CDE7Yn2C.q!a7-x@localhost:27017",
        title="MongoDB movies connection string",
        description="the connection string for the mongo database",
        env="MONGODB_CONNECTION_STRING",
    )
    mongo_database_name: str = Field(
        "movie_track_db",
        title="MongoDB movies Database name",
        description="the database name for the mongoDB Movie Datacase",
        env="MONGODB_CONNECTION_NAME",
    )
