""" Test cases for the movie repository using MongoDB. """

import pytest


from api._test.repository.fixture import mongo_movie_repo_fixture
from api.entities.movies import Movie


@pytest.mark.asyncio
async def test_create(mongo_movie_repo_fixture):
    """
    Test creating a movie in the repository.
    """
    await mongo_movie_repo_fixture.create(
        movie=Movie(
            movie_id="first",
            title="MY MOvie",
            description="description of movie",
            release_year="2015",
            watched=True,
        )
    )
    movie: Movie = await mongo_movie_repo_fixture.get_by_id("first")
    assert movie == Movie(
        movie_id="first",
        title="MY MOvie",
        description="description of movie",
        release_year="2015",
        watched=True,
    )
    await mongo_movie_repo_fixture.delete("first")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial_movies, movie_id, expected_result",
    [
        pytest.param(
            [
                Movie(
                    movie_id="first",
                    title="MY MOvie",
                    description="description of movie",
                    release_year="2015",
                    watched=True,
                ),
                Movie(
                    movie_id="second",
                    title="MY second MOvie",
                    description="second description of movie",
                    release_year="2019",
                    watched=True,
                ),
            ],
            "second",
            Movie(
                movie_id="second",
                title="MY second MOvie",
                description="second description of movie",
                release_year="2019",
                watched=True,
            ),
            id="movie-found",
        ),
    ],
)
async def test_get_by_id(
    mongo_movie_repo_fixture, initial_movies, movie_id, expected_result
):
    """
    Test getting a movie by id from the repository.
    """
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)

    movie: Movie = await mongo_movie_repo_fixture.get_by_id(movie_id)
    assert movie == expected_result

@pytest.mark.parametrize(
    "initial_movies,searched_title,expected_movies",
    [
        pytest.param([], "random title", [], id="empty-case"),
        pytest.param(
            [
                Movie(
                    movie_id="first",
                    title="My Movie",
                    description="My Movie Description",
                    release_year=2022,
                    watched=True,
                ),
                Movie(
                    movie_id="second",
                    title="My Second Movie",
                    description="My Second Movie Description",
                    release_year=2023,
                    watched=False,
                ),
                Movie(
                    movie_id="first_remake",
                    title="My Movie",
                    description="My Movie Description remake of the first movie from 2022",
                    release_year=2025,
                    watched=True,
                ),
            ],
            "My Movie",
            [
                Movie(
                    movie_id="first",
                    title="My Movie",
                    description="My Movie Description",
                    release_year=2022,
                    watched=True,
                ),
                Movie(
                    movie_id="first_remake",
                    title="My Movie",
                    description="My Movie Description remake of the first movie from 2022",
                    release_year=2025,
                    watched=True,
                ),
            ],
            id="found-movies",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(
    mongo_movie_repo_fixture, initial_movies, searched_title, expected_movies
):
    """ Test getting movies by title from the repository."""
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)
    movies = await mongo_movie_repo_fixture.get_by_title(title=searched_title)
    assert movies == expected_movies
# @pytest.mark.parametrize(
#     "initial_movies, searched_title, expected_movies",
#     [
#         pytest.param([], "random title", [], id="empty-case"),
#         pytest.param(
#             [
#                 Movie(
#                     movie_id="first",
#                     title="My Movie",
#                     description="My movie description",
#                     release_year="2022",
#                     watched=True,
#                 ),
#                 Movie(
#                     movie_id="first_remake",
#                     title="My Movie",
#                     description="description of remaken movie",
#                     release_year="2025",
#                     watched=True,
#                 ),
#             ],
#             "My Movie",
#             [
#                 Movie(
#                     movie_id="first",
#                     title="My Movie",
#                     description="description of movie",
#                     release_year="2015",
#                     watched=True,
#                 ),
#                 Movie(
#                     movie_id="first_remake",
#                     title="My Movie",
#                     description="description of remaken movie",
#                     release_year="2025",
#                     watched=True,
#                 ),
#             ],
#             id="found-movies",
#         ),
#     ],
# )
# @pytest.mark.asyncio
# async def test_get_by_title(
#     mongo_movie_repo_fixture, initial_movies, searched_title, expected_movies
# ):
#     """
#     Test getting movies by title from the repository.
#     """
#     for movie in initial_movies:
#         await mongo_movie_repo_fixture.create(movie)
#     movies = await mongo_movie_repo_fixture.get_by_title(title=searched_title)
#     assert movies == expected_movies
    # movies = await mongo_movie_repo_fixture.get_by_title(title=searched_title)

    # assert len(movies) == len(expected_movies)
    # for movie, expected_movie in zip(movies, expected_movies):
    #     assert movie.movie_id == expected_movie.movie_id
    #     assert movie.title == expected_movie.title
    #     assert movie.description == expected_movie.description
    #     assert movie.release_year == expected_movie.release_year
    #     assert movie.watched == expected_movie.watched


@pytest.mark.asyncio
async def test_update():
    """
    Test updating a movie in the repository.
    """
    pass


@pytest.mark.asyncio
async def test_delete():
    """
    Test deleting a movie from the repository.
    """
    pass
