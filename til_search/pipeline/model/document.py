from pydantic import BaseModel


class Document(BaseModel):
    id: str
    title: list[str]
    content: str
    path: str