"""This module contains fixtures for the repository tests."""

import asyncio
import secrets

import pytest
from starlette.testclient import TestClient

from api.api import create_app
from api.repository.movie.memory import MemoryMovieRepository
from api.repository.movie.mongo import MongoMovieRepository


@pytest.fixture
def test_client_fixture():
    """Return a TestClient instance."""
    return TestClient(app=create_app())


@pytest.fixture
def mongo_movie_repo_fixture():
    """
    Create a new database for testing and drop it after the test is done.
    """
    random_database_name = secrets.token_hex(8)
    # repo = MongoMovieRepository(
    #     connection_string = "mongodb://movietracker_dbAdmin:CDE7Yn2C.q!a7-x@localhost:27017",
    #     database = random_database_name
    # )
    # yield repo
    # loop = asyncio.get_running_loop()
    # loop.run_until_complete(repo._client.drop_database(random_database_name))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    repo = MongoMovieRepository(
        connection_string="mongodb://movietracker_dbAdmin:CDE7Yn2C.q!a7-x@localhost:27017",
        database=random_database_name,
    )

    yield repo

    # Close the event loop after the test
    loop.close()


@pytest.fixture()
def memory_movie_repo_fixture():
    """Return a MemoryMovieRepository instance."""
    return MemoryMovieRepository()
