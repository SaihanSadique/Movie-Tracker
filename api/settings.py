"""Settings for the API."""

from functools import lru_cache

from pydantic import BaseSettings, Field


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

    def __hash__(self) -> int:
        return 1


@lru_cache()
def settings_instance():
    """Settings instance to be used as a FastAPI dependency.
    LRU cache is used to store the settings instance to avoid creating a new instance every
    time it is requested.
    """
    return Settings()
