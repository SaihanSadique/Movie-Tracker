"""
Class for movie created response
"""

from pydantic import BaseModel


class MovieCreatedResponse(BaseModel):
    """
    Movie created response
    """

    movie_id: str
