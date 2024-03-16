"""
This file contains the tests for the movie repository.
"""

import pytest
from api.entities.movies import Movie
from api.repository.movie.abstractions import RepositoryException

from api.repository.movie.movies import MemoryMovieRepository


def test_create():
    """Test the creation of a movie in the repository."""
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test_id",
        title="test_title",
        description="test_description",
        release_year=2021,
        watched=False,
    )
    repo.create(movie)
    assert repo.get_by_id("test_id") is movie


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
def test_get_by_id(movies_seed, movie_id, expected_result):
    """Test the retrieval of a movie by its id."""
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        repo.create(movie)
    movie = repo.get_by_id(movie_id=movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed,movie_title,expected_results",
    [
        pytest.param([], "some-title", None, id="empty-results"),
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
            "some-title",
            None,
            id="empty-results-2",
        ),
    ],
)
def test_get_by_title(movies_seed, movie_title, expected_results):
    """Test the retrieval of a movie by its title."""
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        repo.create(movie)
    assert repo.get_by_title(movie_title) == expected_results


def test_delete():
    """Test the deletion of a movie from the repository."""
    repo = MemoryMovieRepository()
    repo.create(
        Movie(
            movie_id="test_id",
            title="test_title",
            description="test_description",
            release_year=2021,
            watched=False,
        )
    )
    repo.delete("test_id")
    assert repo.get_by_id("test_id") is None


def test_update_success():
    """Test the successful update of a movie in the repository."""
    repo = MemoryMovieRepository()
    repo.create(
        Movie(
            movie_id="my-id-2",
            title="test_title",
            description="test_description",
            release_year=2021,
            watched=False,
        )
    )
    repo.update(
        movie_id="my-id-2",
        update_parameteres={
            "title": "my-updated-movie",
            "description": "my updated description",
            "release_year": 2010,
            "watched": True,
        },
    )
    movie = repo.get_by_id("my-id-2")
    assert movie == Movie(
        movie_id="my-id-2",
        title="my-updated-movie",
        description="my updated description",
        release_year=2010,
        watched=True,
    )


def test_update_fail():
    """Test the failed update of a movie in the repository."""
    repo = MemoryMovieRepository()
    repo.create(
        Movie(
            movie_id="test_id",
            title="test_title",
            description="test_description",
            release_year=2021,
            watched=False,
        )
    )
    with pytest.raises(RepositoryException):
        repo.update(movie_id="my-id-2", update_parameteres={"id": "fail"})