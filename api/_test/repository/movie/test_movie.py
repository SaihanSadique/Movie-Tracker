"""
This file contains the tests for the movie repository.
"""

import pytest
from api.entities.movies import Movie
from api.repository.movies import MemoryMovieRepository


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


@pytest.mark.parameterize(
    "movies_seed,movie_id,expected_result",
    [pytest.param([], "my-id", "None", id="empty")],
)
def test_get_by_id(movies_seed, movie_id, expected_result):
    """Test the retrieval of a movie by its id."""
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        repo.create(movie)
    movie = repo.get_by_id(movie_id=movie_id)
    assert movie == expected_result


def test_get_by_title():
    """Test the retrieval of a movie by its title."""


def test_delete():
    """Test the deletion of a movie from the repository."""


def test_update():
    """Getter for the movie release year"""
