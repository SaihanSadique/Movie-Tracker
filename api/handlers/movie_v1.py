"""
This file contains the FastAPI router for the movie API. version 1.
"""

from functools import lru_cache
import uuid
from fastapi import APIRouter, Body, Depends

from api.dto.movie import CreateMovieBody
from api.entities.movies import Movie
from api.repository.movie.abstractions import MovieRepository
from api.repository.movie.mongo import MongoMovieRepository
from api.responses.movie import MovieCreatedResponse
from api.settings import Settings

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@lru_cache()
def settings_instance():
    """Creates a new instance of the settings."""
    return Settings()


def movie_repository(settings: Settings = Depends(settings_instance)):
    """Creates a new instance of the movie repository."""
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def create_movie(
    movie: CreateMovieBody = Body(..., title="movie", description="Movie details"),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Creates a new movie
    """

    movie_id = str(uuid.uuid4())
    await repo.create(
        movie=Movie(
            movie_id=movie_id,
            title=movie.title,
            description=movie.description,
            release_year=movie.release_year,
            watched=movie.watched,
        )
    )
    return MovieCreatedResponse(movie_id=movie_id)
