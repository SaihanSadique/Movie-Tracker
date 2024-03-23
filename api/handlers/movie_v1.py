"""
This file contains the FastAPI router for the movie API. version 1.
"""

import uuid
from fastapi import APIRouter, Body

from api.dto.movie import CreateMovieBody
from api.entities.movies import Movie
from api.repository.movie.mongo import MongoMovieRepository
from api.responses.movie import MovieCreatedResponse

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def create_movie(
    movie: CreateMovieBody = Body(..., title="movie", description="Movie details")
):
    """
    Creates a new movie
    """
    repo = MongoMovieRepository("mongodb://movietracker_dbAdmin:CDE7Yn2C.q!a7-x@localhost:27017")

    movie_id = str(uuid.uuid4())
    await repo.create(movie=Movie(
        movie_id= movie_id,
        title = movie.title,
        description = movie.description,
        release_year= movie.release_year,
        watched = movie.watched,
    ))
    return MovieCreatedResponse(movie_id=movie_id)
