""" Test cases for the movie repository using MongoDB. """

import pytest

from api.entities.movies import Movie
from api.repository.movie.mongo import MongoMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MongoMovieRepository(
        connection_string="mongodb://movietracker_dbAdmin:CDE7Yn2C.q!a7-x@localhost:27017",
        database="movie_tracker_db",
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
    pass


@pytest.mark.asyncio
async def test_get_by_title():
    pass


@pytest.mark.asyncio
async def test_update():
    pass


@pytest.mark.asyncio
async def test_delete():
    pass
