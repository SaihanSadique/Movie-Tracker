""" Test cases for the movie repository using MongoDB. """

import pytest

from api.entities.movies import Movie
from api.repository.movie.mongo import MongoMovieRepository


@pytest.mark.asyncio
async def test_create():
    """
    Test creating a movie in the repository.
    """
    repo = MongoMovieRepository(
        connection_string="mongodb://movietracker_dbAdmin:CDE7Yn2C.q!a7-x@localhost:27017",
        database="movie_track_db",
        # mongodb://myUsername:myPassword@localhost:27017/myDatabase?authSource=admin
        # connection_string="mongodb://localhost:27017", database="movie_tracker_db"
    )
    await repo.create(
        movie=Movie(
            movie_id="first",
            title="MY MOvie",
            description="description of movie",
            release_year="2015",
            watched=True,
        )
    )
    movie: Movie = await repo.get_by_id("first")
    assert movie == Movie(
        movie_id="first",
        title="MY MOvie",
        description="description of movie",
        release_year="2015",
        watched=True,
    )


@pytest.mark.asyncio
async def test_get_by_id():
    """
    Test getting a movie by id from the repository.
    """


@pytest.mark.asyncio
async def test_get_by_title():
    """
    Test getting movies by title from the repository.
    """


@pytest.mark.asyncio
async def test_update():
    """
    Test updating a movie in the repository.
    """


@pytest.mark.asyncio
async def test_delete():
    """
    Test deleting a movie from the repository.
    """
