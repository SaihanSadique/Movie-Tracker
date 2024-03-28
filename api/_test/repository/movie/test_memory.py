"""
This file contains the tests for the movie repository.
"""
# pylint: disable=unused-import , redefined-outer-name
import pytest

from api._test.repository.fixture import memory_movie_repo_fixture

from api.entities.movies import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create():
    """Test the creation of a movie in the repository."""
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test_id",
        title="test_title",
        description="test_description",
        release_year=2021,
        watched=False,
    )
    await repo.create(movie)
    assert await repo.get_by_id("test_id") is movie


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movies_seed,movie_id,expected_result",
    [
        pytest.param([], "my-id", None, id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="test_title",
                    description="test_description",
                    release_year=2021,
                    watched=False,
                )
            ],
            "my-id",
            Movie(
                movie_id="my-id",
                title="test_title",
                description="test_description",
                release_year=2021,
                watched=False,
            ),
            id="actual-movie",
        ),
    ],
)
async def test_get_by_id(movies_seed, movie_id, expected_result):
    """Test the retrieval of a movie by its id."""
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    movie = repo.get_by_id(movie_id=movie_id)
    assert await movie == expected_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movies_seed,movie_title,expected_results",
    [
        pytest.param([], "some-title", [], id="empty-results"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched=True,
                )
            ],
            "some-title",
            [],
            id="empty-results-2",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched=True,
                ),
                Movie(
                    movie_id="my-id-2",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched=True,
                ),
            ],
            "My Movie",
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched=True,
                ),
                Movie(
                    movie_id="my-id-2",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched=True,
                ),
            ],
            id="results",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(movies_seed, movie_title, expected_results):
    """Test the retrieval of a movie by its title."""
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    result = await repo.get_by_title(title=movie_title)
    assert result == expected_results

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "skip,limit,expected_results",
    [
        pytest.param(
            0,
            0,
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched= False,
                ),
                Movie(
                    movie_id="my-id-2",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched= False,
                ),
                Movie(
                    movie_id="my-id-3",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched= False,
                ),
            ],
        ),
        pytest.param(
            0,
            1,
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched= False,
                )
            ],
        ),
        pytest.param(
            1,
            1,
            [
                Movie(
                    movie_id="my-id-2",
                    title="My Movie",
                    description="My description",
                    release_year=1990,
                    watched= False,
                )
            ],
        ),
    ],
)
async def test_get_by_title_pagination(
    memory_movie_repo_fixture, skip, limit, expected_results
):
    """Test the retrieval of a movie by its title with pagination."""
    movie_seed = [
        Movie(
            movie_id="my-id",
            title="My Movie",
            description="My description",
            release_year=1990,
            watched= False,
        ),
        Movie(
            movie_id="my-id-2",
            title="My Movie",
            description="My description",
            release_year=1990,
            watched= False,
        ),
        Movie(
            movie_id="my-id-3",
            title="My Movie",
            description="My description",
            release_year=1990,
            watched= False,
        ),
    ]
    for movie in movie_seed:
        await memory_movie_repo_fixture.create(movie)
    results = await memory_movie_repo_fixture.get_by_title(
        title="My Movie", skip=skip, limit=limit
    )
    assert results == expected_results

# @pytest.mark.asyncio()
# @pytest.mark.parametrize(
#     "movies_seed,movie_title,expected_results",
#     [
#         pytest.param([], "some-title", None, id="empty-results"),
#         pytest.param(
#             [
#                 Movie(
#                     movie_id="my-id",
#                     title="test_title",
#                     description="test_description",
#                     release_year=2021,
#                     watched=False,
#                 )
#             ],
#             "some-title",
#             None,
#             id="empty-results-2",
#         ),
#         pytest.param(
#             [
#                 Movie(
#                     movie_id="my-id",
#                     title="My Movie",
#                     description="test_description",
#                     release_year=2021,
#                     watched=False,
#                 )
#             ],
#             "My Movie",
#             [
#                 Movie(
#                     movie_id="my-id",
#                     title="My Movie",
#                     description="test_description",
#                     release_year=2021,
#                     watched=False,
#                 )
#             ],
#             id="results",
#         ),
#     ],
# )
# async def test_get_by_title(movies_seed, movie_title, expected_results):
#     """Test the retrieval of a movie by its title."""
#     repo = MemoryMovieRepository()
#     for movie in movies_seed:
#         await repo.create(movie)
#     assert await repo.get_by_title(movie_title) == expected_results


@pytest.mark.asyncio()
async def test_delete():
    """Test the deletion of a movie from the repository."""
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="test_id",
            title="test_title",
            description="test_description",
            release_year=2021,
            watched=False,
        )
    )
    await repo.delete("test_id")
    assert await repo.get_by_id("test_id") is None


@pytest.mark.asyncio()
async def test_update_success():
    """Test the successful update of a movie in the repository."""
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id-2",
            title="test_title",
            description="test_description",
            release_year=2021,
            watched=False,
        )
    )
    await repo.update(
        movie_id="my-id-2",
        update_parameteres={
            "title": "my-updated-movie",
            "description": "my updated description",
            "release_year": 2010,
            "watched": True,
        },
    )
    movie = repo.get_by_id("my-id-2")
    assert await movie == Movie(
        movie_id="my-id-2",
        title="my-updated-movie",
        description="my updated description",
        release_year=2010,
        watched=True,
    )


@pytest.mark.asyncio()
async def test_update_fail():
    """Test the failed update of a movie in the repository."""
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="test_id",
            title="test_title",
            description="test_description",
            release_year=2021,
            watched=False,
        )
    )
    with pytest.raises(RepositoryException):
        await repo.update(movie_id="my-id-2", update_parameteres={"id": "fail"})
