""" This module defines CRUD operations for a repository."""

import abc
import typing

from api.entities.movies import Movie


class RepositoryException(Exception):
    """Base class for repository exceptions."""


class MovieRepository(abc.ABC):
    """
    Abstract base class that defines a common interface for movie repositories.

    This class provides methods for creating, retrieving, and deleting movies.
    Concrete subclasses must implement these methods to provide specific storage
    mechanisms (e.g., database, file system).

    """

    async def create(self, movie: Movie) -> bool:
        """
        Inserts the movie into the database.
        """
        raise NotImplementedError

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """
        Returns a movie by its id and if not found, returns None.
        Raises RepositoryException of Failure.
        """
        raise NotImplementedError

    async def get_by_title(self, title: str) -> typing.List[Movie]:
        """
        Returns a list of movies which share the same title and if not found, returns None.
        """
        raise NotImplementedError

    async def delete(self, movie_id: str):
        """
        Deletes a movie by its id.
        Raises RepositoryException of Failure.
        """
        raise NotImplementedError

    async def update(self, movie_id: str, update_parameteres: dict):
        """
        Updates a movie.
        """
        raise NotImplementedError
