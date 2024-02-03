from pydantic import BaseModel


class PostUrl(BaseModel):
  longUrl: str
  customUrl: str | None = None
