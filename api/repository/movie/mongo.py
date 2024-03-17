"""
This module contains the implementation of the MovieRepository interface using an in-memory storage
"""

import typing

import motor.motor_asyncio

from api.entities.movies import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MongoMovieRepository(MovieRepository):
    """MongoMovieRepository implements the repository pattern for our movie enitity using MongoDB"""

    def __init__(self, connection_string: str = "mongodb://localhost:27017") -> None:
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client["movie_tracker_db"]
        # movies collection which holds the movie documents
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        await self._movies.insert_one(
            {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_year": movie.release_year,
                "watched": movie.watched,
            }
        )

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        document = await self._movies.find_one({"id": movie_id})
        if document:
            return Movie(
                movie_id=document.get["id"],
                title=document.get["title"],
                description=document.get["description"],
                release_year=document.get["release_year"],
                watched=document.get["watched"],
            )
        return None

    async def get_by_title(self, title: str) -> typing.List[Movie]:
        return_value: typing.List[Movie] = []
        document_cursor = self._movies.find({"title": title})
        # iterate through documents
        async for document in document_cursor:
            return_value.append(
                Movie(
                    movie_id=document.get["id"],
                    title=document.get["title"],
                    description=document.get["description"],
                    release_year=document.get["release_year"],
                    watched=document.get["watched"],
                )
            )

    async def update(self, movie_id: str, update_parameteres: dict):
        if id in update_parameteres.keys():
            raise RepositoryException("Cannot update movie id")
        result = await self._movies.update_one(
            {"id": movie_id}, {"$set": update_parameteres}
        )
        if result.modified_count == 0:
            raise RepositoryException(f"Movie {movie_id} not found")

    async def delete(self, movie_id: str):
        await self._movies.delete_one({"id": movie_id})
