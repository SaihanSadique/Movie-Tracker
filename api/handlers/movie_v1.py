"""
This file contains the FastAPI router for the movie API. version 1.
"""

import typing
import uuid
from collections import namedtuple
from functools import lru_cache

from fastapi import APIRouter, Body, Depends, Path, Query
from starlette.responses import Response

from api.dto.detail import DetailResponse
from api.dto.movie import (CreateMovieBody, MovieCreatedResponse,
                           MovieResponse, MovieUpdateBody)
from api.entities.movies import Movie
from api.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)
from api.repository.movie.mongo import MongoMovieRepository
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


def pagination_params(
    skip: int = Query(0, title="Skip", description="The number of items to skip", ge=0),
    limit: int = Query(
        1000,
        title="Limit",
        description="The limit of the number of items returned",
        le=1000,
    ),
):
    """Returns a named tuple with the pagination parameters."""
    Pagination = namedtuple("Pagination", ["skip", "limit"])
    return Pagination(skip=skip, limit=limit)


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


@router.get("/", response_model=typing.List[MovieResponse])
async def get_movies_by_title(
    title: str = Query(
        ..., title="Title", description="Title of the movie to search for", min_length=3
    ),
    pagination: namedtuple = Depends(pagination_params),
    repo: MovieRepository = Depends(movie_repository),
):
    """Returns a list of movies that match the title provided.
    If no movies are found, an empty list is returned."""
    movies = await repo.get_by_title(
        title, skip=pagination.skip, limit=pagination.limit
    )
    movies_return_value = []
    for movie in movies:
        movies_return_value.append(
            MovieResponse(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                release_year=movie.release_year,
                watched=movie.watched,
            )
        )
    return movies_return_value


@router.patch(
    "/{movie_id}",
    responses={200: {"model": DetailResponse}, 400: {"model": DetailResponse}},
)
async def patch_movie(
    movie_id: str = Path(
        ..., title="Movie ID", description="The ID of the movie to update"
    ),
    update_parameteres: MovieUpdateBody = Body(
        ..., title="Update body", description="The parameters to update for the movie."
    ),
    repo: MovieRepository = Depends(movie_repository),
):
    """Updates a movie with the provided parameters."""
    try:
        update_dict = update_parameteres.dict(exclude_unset=True, exclude_none=True)
        await repo.update(movie_id=movie_id, update_parameteres=update_dict)
    except RepositoryException as e:
        return DetailResponse(message=str(e))


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(
    movie_id: str = Path(
        ..., title="Movie ID", description="The ID of the movie to update"
    ),
    repo: MovieRepository = Depends(movie_repository),
):
    """Deletes a movie with the provided ID."""
    await repo.delete(movie_id=movie_id)
    return Response(status_code=204)
