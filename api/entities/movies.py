"""This module contains the movie class"""


class Movie:
    """
    Represents a movie with attributes for identification, metadata, and watch status.
    Attributes:
        id (str): Unique identifier for the movie.
        title (str): Title of the movie.
        description (str): Optional description of the movie.
        release_year (int): Year the movie was released.
        watched (bool): Indicates whether the movie has been watched (True) or not (False).
    """

    def __init__(
        self,
        *,
        movie_id: str,
        title: str,
        description: str,
        release_year: int,
        watched: bool
    ):
        if movie_id is None:
            raise ValueError("Movie id is required")
        self._id = movie_id
        self._title = title
        self._description = description
        self._release_year = release_year
        self._watched = watched

    @property
    def id(self) -> str:
        """Getter for the movie id"""
        return self._id

    @property
    def title(self) -> str:
        """Getter for the movie title"""
        return self._title

    @property
    def description(self) -> str:
        """Getter for the movie description"""
        return self._description

    @property
    def release_year(self) -> int:
        """Getter for the movie release year"""
        return self._release_year

    @property
    def watched(self) -> bool:
        """Getter for the movie watched status"""
        return self._watched
