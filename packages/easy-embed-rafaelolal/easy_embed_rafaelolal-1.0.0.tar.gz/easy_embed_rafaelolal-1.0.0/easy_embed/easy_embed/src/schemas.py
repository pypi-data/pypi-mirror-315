from pydantic import BaseModel


class CreateRequest(BaseModel):
    doc: str
    index: int
    collection: str


class ReadRequest(BaseModel):
    q: str
    docs: list[str] | None = None
    collection: str | None = None
    k: int


class UpdateRequest(BaseModel):
    index: int
    collection: str
    doc: str | None = None


class DeleteRequest(BaseModel):
    index: int
    collection: str
