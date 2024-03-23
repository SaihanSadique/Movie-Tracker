"""This module contains the DTOs for the movie endpoints."""

from pydantic import BaseModel


class CreateMovieBody(BaseModel):
    """CreateMovieBody is used as the body for the create movie endpoint."""

    title: str
    description: str
    release_year: int
    watched: bool = False
