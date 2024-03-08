"""Creates a response model for the endpoints."""

from pydantic import BaseModel


class DetailResponse(BaseModel):
    """
    Response model for the endpoints.
    """

    message: str
