"""
This module contains the implementation of the MovieRepository interface using an in-memory storage
"""

import typing

from api.entities.movies import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    """
    This class provides an in-memory implementation of the MovieRepository interface.
    """

    def __init__(self):
        self._storage = {}

    async def create(self, movie: Movie) -> bool:
        self._storage[movie.id] = movie

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    async def get_by_title(self, title: str) -> typing.List[Movie]:
        return_value = []
        for _, value in self._storage.items():
            if value.title == title:
                return_value.append(value)

    async def delete(self, movie_id: str):
        self._storage.pop(movie_id, None)

    async def update(self, movie_id: str, update_parameteres: dict):
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"Movie {movie_id} not found")
        for key, value in update_parameteres.items():
            if key == "id":
                raise RepositoryException("Cannot update movie id")
            if hasattr(movie, key):
                setattr(movie, f"_{key}", value)  # Update the movie entity field
