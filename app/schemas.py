from pydantic import BaseModel


class RepositorySchema(BaseModel):
    name: str
    owner: str
    stars: int
    url: str


class SearchResponseSchema(BaseModel):
    query: str
    repos_count: int
    total_stars: int
    average_stars: float
    top_repo: str | None
    repos: list[RepositorySchema]
