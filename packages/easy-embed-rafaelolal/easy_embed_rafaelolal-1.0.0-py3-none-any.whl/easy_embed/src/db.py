from typing import Annotated

from fastapi import Depends
from sqlalchemy import JSON, Column
from sqlmodel import (
    Field,
    Index,
    Session,
    SQLModel,
    UniqueConstraint,
    create_engine,
    select,
)


class Embedding(SQLModel, table=True):
    id: int = Field(primary_key=True)
    index: int
    doc: str
    embedding: list[float] = Field(sa_column=Column(JSON))
    collection: str = Field(index=True)  # Add indexed collection field

    # Create composite primary key for id and collection
    __table_args__ = (Index("idx_collection_id", "collection", "id"),)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_embedding(
    session: Session,
    doc: str,
    embedding: list[float],
    index: int,
    collection: str,
):
    existing = session.exec(
        select(Embedding).where(
            (Embedding.index == index) & (Embedding.collection == collection)
        )
    ).first()

    if existing:
        raise ValueError(
            f"Embedding with index {index} in collection {collection} already exists"
        )

    db_embedding = Embedding(
        doc=doc, embedding=embedding, index=index, collection=collection
    )
    session.add(db_embedding)
    session.commit()
    session.refresh(db_embedding)
    return db_embedding


def read_collection(session: Session, collection: str) -> list[Embedding]:
    result = session.exec(
        select(Embedding)
        .where(Embedding.collection == collection)
        .order_by(Embedding.index)
    ).all()

    if not result:
        raise ValueError(f"Collection {collection} not found")

    return result


def update_embedding(
    session: Session,
    index: int,
    collection: str,
    doc: str,
    embedding_values: list[float],
) -> Embedding:
    statement = select(Embedding).where(
        (Embedding.index == index) & (Embedding.collection == collection)
    )
    db_embedding = session.exec(statement).first()
    if not db_embedding:
        raise ValueError(
            f"Embedding with index {index} in collection {collection} not found"
        )

    db_embedding.doc = doc
    db_embedding.embedding = embedding_values

    session.add(db_embedding)
    session.commit()
    session.refresh(db_embedding)
    return db_embedding


def delete_embedding(
    session: Session,
    index: int,
    collection: str,
) -> Embedding:
    statement = select(Embedding).where(
        (Embedding.index == index) & (Embedding.collection == collection)
    )
    db_embedding = session.exec(statement).first()
    if not db_embedding:
        raise ValueError(
            f"Embedding with index {index} in collection {collection} not found"
        )

    session.delete(db_embedding)
    session.commit()
    return db_embedding
