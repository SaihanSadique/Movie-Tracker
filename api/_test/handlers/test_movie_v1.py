""" Test cases for the movie_v1 api endpoint. """

# pylint: disable=unused-import , redefined-outer-name
import functools
import pytest

# from api._test.repository.fixture import test_client
from api._test.repository.fixture import test_client_fixture
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
    movie = await repo.get_by_id(movie_id = movie_id)
    assert movie is not None
    

