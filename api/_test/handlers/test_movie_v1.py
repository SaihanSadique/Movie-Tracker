""" Test cases for the movie_v1 api endpoint. """

# pylint: disable=unused-import , redefined-outer-name
import functools
import pytest

# from api._test.repository.fixture import test_client
from api._test.repository.fixture import test_client_fixture
from api.entities.movies import Movie
from api.handlers.movie_v1 import movie_repository
from api.repository.movie.memory import MemoryMovieRepository


def memory_repository_dependency(dependency):
    """Dependency override for the memory repository."""
    return dependency


@pytest.mark.asyncio()
async def test_create_movie(test_client_fixture):
    """Test creating a movie."""
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency
    result = test_client_fixture.post(
        "/api/v1/movies/",
        json={
            "title": "The Shawshank Redemption",
            "description": "string",
            "release_year": 1994,
            "watched": "true",
        },
    )
    movie_id = result.json().get("id")
    assert result.status_code == 201
    movie = await repo.get_by_id(movie_id=movie_id)
    assert movie is not None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_json",
    [
        (
            {
                "description": "string",
                "release_year": 1994,
                "watched": "true",
            },
        ),
        (
            {
                "title": "The Shawshank Redemption",
                "release_year": 1994,
                "watched": "true",
            }
        ),
    ],
)
async def test_create_movie_validation_error(test_client_fixture, movie_json):
    """Test creating a movie with validation errors."""

    # setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency

    # result
    result = test_client_fixture.post(
        "/api/v1/movies/",
        json=movie_json,
    )

    # assertion
    assert result.status_code == 422


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_seed, movie_id, expected_status_code, expected_result",
    [
        pytest.param(
            [],
            "random",
            404,
            {"message": "Movie with ID random not found"},
            id="not-found",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="found",
                    title="The Shawshank Redemption",
                    description="string",
                    release_year=1994,
                    watched=True,
                )
            ],
            "found",
            200,
            {
                "description": "string",
                "id": "found",
                "release_year": 1994,
                "title": "The Shawshank Redemption",
                "watched": True,
            },
            id="found",
        ),
    ],
)
async def test_get_movie_by_id(
    test_client_fixture, movie_seed, movie_id, expected_status_code, expected_result
):
    """Test getting a movie by id."""

    # setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # Test
    result = test_client_fixture.get(f"/api/v1/movies/{movie_id}")

    # Assert
    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_seed,movie_title,skip, limit, expected_result",
    [
        pytest.param([], "movie_title", 0, 1000, [], id="empty-result"),
        pytest.param(
            [
                Movie(
                    movie_id="1",
                    title="movie title",
                    description="Movie Description",
                    release_year=2000,
                    watched=True,
                ),
                Movie(
                    movie_id="2",
                    title="movie title",
                    description="Movie Description",
                    release_year=2001,
                    watched=True,
                ),
                Movie(
                    movie_id="3",
                    title="movie title",
                    description="Movie Description",
                    release_year=2002,
                    watched=True,
                ),
                Movie(
                    movie_id="4",
                    title="movie title2",
                    description="Movie Description",
                    release_year=2002,
                    watched=True,
                ),
            ],
            "movie title",
            0,
            1000,
            [
                {
                    "description": "Movie Description",
                    "id": "1",
                    "release_year": 2000,
                    "title": "movie title",
                    "watched": True,
                },
                {
                    "description": "Movie Description",
                    "id": "2",
                    "release_year": 2001,
                    "title": "movie title",
                    "watched": True,
                },
                {
                    "description": "Movie Description",
                    "id": "3",
                    "release_year": 2002,
                    "title": "movie title",
                    "watched": True,
                },
            ],
            id="some-results",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="1",
                    title="movie title",
                    description="Movie Description",
                    release_year=2000,
                    watched=True,
                ),
                Movie(
                    movie_id="2",
                    title="movie title",
                    description="Movie Description",
                    release_year=2001,
                    watched=True,
                ),
                Movie(
                    movie_id="3",
                    title="movie title",
                    description="Movie Description",
                    release_year=2002,
                    watched=True,
                ),
                Movie(
                    movie_id="4",
                    title="movie title2",
                    description="Movie Description",
                    release_year=2002,
                    watched=True,
                ),
            ],
            "movie title",
            1,
            1000,
            [
                {
                    "description": "Movie Description",
                    "id": "2",
                    "release_year": 2001,
                    "title": "movie title",
                    "watched": True,
                },
                {
                    "description": "Movie Description",
                    "id": "3",
                    "release_year": 2002,
                    "title": "movie title",
                    "watched": True,
                },
            ],
            id="some-results-pagination-1-1000",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="1",
                    title="movie title",
                    description="Movie Description",
                    release_year=2000,
                    watched=True,
                ),
                Movie(
                    movie_id="2",
                    title="movie title",
                    description="Movie Description",
                    release_year=2001,
                    watched=True,
                ),
                Movie(
                    movie_id="3",
                    title="movie title",
                    description="Movie Description",
                    release_year=2002,
                    watched=True,
                ),
                Movie(
                    movie_id="4",
                    title="movie title2",
                    description="Movie Description",
                    release_year=2002,
                    watched=True,
                ),
            ],
            "movie title",
            1,
            1,
            [
                {
                    "description": "Movie Description",
                    "id": "2",
                    "release_year": 2001,
                    "title": "movie title",
                    "watched": True,
                },
            ],
            id="some-results-pagination-1-1",
        ),
    ],
)
async def test_get_movies_by_title(
    test_client_fixture, movie_seed, movie_title, skip, limit, expected_result
):
    """Test getting movies by title."""
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency

    for movie in movie_seed:
        await repo.create(movie)

    # Test
    result = test_client_fixture.get(
        f"/api/v1/movies/?title={movie_title}&skip={skip}&limit={limit}"
    )

    # Assertion
    assert result.status_code == 200
    for movie in result.json():
        assert movie in expected_result
    assert len(result.json()) == len(expected_result)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "update_parameters,updated_movie",
    [
        (
            {
                "title": "My Title Update",
                "id": "new test id",
            },
            Movie(
                movie_id="top_movie",
                title="My Title Update",
                description="Needs update",
                release_year=1994,
                watched=True,
            ),
        ),
        (
            {
                "description": "My Desc Update",
                "random": "Test",
            },
            Movie(
                movie_id="top_movie",
                title="Needs Update",
                description="My Desc Update",
                release_year=1994,
                watched=True,
            ),
        ),
        (
            {
                "release_year": 3000,
            },
            Movie(
                movie_id="top_movie",
                title="Needs Update",
                description="Needs update",
                release_year=3000,
                watched=True,
            ),
        ),
        (
            {
                "watched": False,
            },
            Movie(
                movie_id="top_movie",
                title="Needs Update",
                description="Needs update",
                release_year=1994,
                watched=False,
            ),
        ),
    ],
)
async def test_patch_update_movie(
    test_client_fixture, update_parameters, updated_movie
):
    """Test updating a movie."""
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency

    await repo.create(
        Movie(
            movie_id="top_movie",
            title="Needs Update",
            description="Needs update",
            release_year=1994,
            watched=True,
        )
    )

    # Test
    result = test_client_fixture.patch(
        "/api/v1/movies/top_movie", json=update_parameters
    )

    assert result.status_code == 200
    assert result.json() == {"message": "Movie updated"}
    if updated_movie is not None:
        assert await repo.get_by_id(movie_id="top_movie") == updated_movie


@pytest.mark.asyncio()
async def test_patch_update_movie_fail(test_client_fixture):
    """Test updating a movie and failing."""
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency

    # Test
    result = test_client_fixture.patch(
        "/api/v1/movies/top_movie", json={"title": "My Title Update"}
    )
    assert result.status_code == 400
    assert result.json() == {"message": "Movie top_movie not found"}


@pytest.mark.asyncio()
async def test_delete_movie(test_client_fixture):
    """Test deleting a movie using the Delete endpoint."""
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client_fixture.app.dependency_overrides[movie_repository] = patched_dependency

    await repo.create(
        Movie(
            movie_id="top_movie",
            title="Needs Update",
            description="Needs update",
            release_year=1994,
            watched=True,
        )
    )

    # Test
    result = test_client_fixture.delete("/api/v1/movies/top_movie")

    assert result.status_code == 204
    assert await repo.get_by_id(movie_id="top_movie") is None
