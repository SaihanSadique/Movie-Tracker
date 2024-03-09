"""This module contains the movie class"""


class Movie:
    """
    Represents a movie with attributes for identification, metadata, and watch status.
    """

    id: str
    title: str
    description: str
    release_year: int
    watched: bool
