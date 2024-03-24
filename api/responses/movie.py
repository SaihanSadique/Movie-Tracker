"""
Class for movie created response
"""

from pydantic import BaseModel


class MovieCreatedResponse(BaseModel):
    """
    Movie created response
    """

    id: str


class MovieResponse(MovieCreatedResponse):
    """
    Movie response
    """

    title: str
    description: str
    release_year: int
    watched: bool
