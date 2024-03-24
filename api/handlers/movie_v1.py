"""
This file contains the FastAPI router for the movie API. version 1.
"""

from functools import lru_cache
import typing
import uuid
from fastapi import APIRouter, Body, Depends, Query

from api.dto.movie import CreateMovieBody
from api.entities.movies import Movie
from api.repository.movie.abstractions import MovieRepository
from api.repository.movie.mongo import MongoMovieRepository
from api.responses.detail import DetailResponse
from api.responses.movie import MovieCreatedResponse, MovieResponse
from api.settings import Settings, settings_instance

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@lru_cache()
def movie_repository(settings: Settings = Depends(settings_instance)):
    """Creates a new instance of the movie repository.
    LRU cache is used to store the repository instance to avoid creating a new instance every
    time it is requested.
    """
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def post_create_movie(
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
    return MovieCreatedResponse(id=movie_id)


@router.get(
    "/{movie_id}",
    responses={200: {"model": MovieResponse}, 404: {"model": DetailResponse}},
)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(movie_repository)
):
    """Returns a movie if found, otherwise returns a 404 response."""
    movie = await repo.get_by_id(movie_id=movie_id)
    if movie is None:
        return DetailResponse(message=f"Movie  with id {movie_id} is not found")
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        release_year=movie.release_year,
        watched=movie.watched,
    )


router.get("/", response_model=typing.List[MovieResponse])


async def get_movies_by_title(
    title: str = Query(
        ..., title="Title", description="Title of the movie to search for", min_length=3
    )
):
    """Returns a list of movies that match the title provided.
        If no movies are found, an empty list is returned."""
    return []
