"""This module contains fixtures for the repository tests."""

import asyncio
import secrets
import pytest


from api.repository.movie.mongo import MongoMovieRepository


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