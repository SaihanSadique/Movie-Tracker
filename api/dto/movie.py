"""This module contains the DTOs for the movie endpoints."""

# pylint: disable=no-self-argument

from pydantic import BaseModel, validator

class CreateMovieBody(BaseModel):
    """DTO for creating a movie."""

    title: str
    description: str
    release_year: int
    watched: bool = False

    @validator("title")
    def title_length_gt_three(cls, v):
        """Validator to ensure title is at least 4 characters long."""
        if len(v) < 4:
            raise ValueError("Title must be at least 4 characters long")
        return v

    @validator("description")
    def description_length_gt_three(cls, v):
        """Validator to ensure title is at least 4 characters long."""
        if len(v) < 4:
            raise ValueError("description must be at least 4 characters long")
        return v

    # @validator("release_year")
    # def release_year(cls, v):
    #     """Validator to ensure release year is a positive integer."""
    #     if v < 1900:
    #         raise ValueError("Release year must be greater than 1900")
    #     return v

class MovieCreatedResponse(BaseModel):
    """DTO for the response when a movie is created."""
    id: str


class MovieResponse(MovieCreatedResponse):
    """DTO for the response when a movie is retrieved."""
    title: str
    description: str
    release_year: int
    watched: bool
