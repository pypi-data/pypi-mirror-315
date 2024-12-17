from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from numpy import ndarray
from torch import Tensor, topk
from torch.nn.functional import cosine_similarity

from .db import (
    Embedding,
    SessionDep,
    create_db_and_tables,
    create_embedding,
    delete_embedding,
    read_collection,
    update_embedding,
)
from .main import App
from .schemas import CreateRequest, DeleteRequest, ReadRequest, UpdateRequest

api = FastAPI()
app = App()

api.add_middleware(
    CORSMiddleware,
    allow_origins=app.allow_origins,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
    max_age=3600,
)


@api.on_event("startup")
def on_startup():
    create_db_and_tables()


@api.post("/create")
def create_api(request: CreateRequest, session: SessionDep) -> dict:
    # try:
    created = create_embedding(
        session=session,
        doc=request.doc,
        embedding=tolist(app.encode(request.doc, convert_to_tensor=True)),
        index=request.index,
        collection=request.collection,
    )

    return {
        "status": "success",
    }


# except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))


@api.post("/read")
def read_api(request: ReadRequest, session: SessionDep) -> dict:
    try:
        if request.docs and request.collection:
            raise HTTPException(
                status_code=400,
                detail="Only one of 'docs' or 'collection' should be provided",
            )

        search = []
        if request.docs:
            search = enumerate(request.docs)
        if request.collection:
            search = (
                (db_embedding.index, db_embedding.doc)
                for db_embedding in read_collection(
                    session, request.collection
                )
            )

        search = tuple(search)

        if not search:
            raise HTTPException(
                status_code=400, detail="No documents to search"
            )

        q = app.encode(request.q, convert_to_tensor=True)
        docs = app.encode(
            tuple(item[1] for item in search), convert_to_tensor=True
        )
        similarities = cosine_similarity(q.unsqueeze(0), docs, dim=-1)
        scores, indices = topk(similarities, min(request.k, len(docs)))

        return {
            "scores": tolist(scores),
            "indices": [search[i][0] for i in tolist(indices)],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.put("/update")
def update_api(
    update_data: UpdateRequest,
    session: SessionDep,
) -> dict:
    try:
        updated = update_embedding(
            session,
            index=update_data.index,
            collection=update_data.collection,
            doc=update_data.doc,
            embedding_values=tolist(
                app.encode(update_data.doc, convert_to_tensor=True)
            ),
        )

        return {
            "status": "success",
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.delete("/delete")
def delete_api(
    delete_data: DeleteRequest,
    session: SessionDep,
) -> Embedding:
    try:
        deleted = delete_embedding(
            session,
            index=delete_data.index,
            collection=delete_data.collection,
        )

        return deleted

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def tolist(data: Tensor | ndarray) -> list:
    if isinstance(data, Tensor):
        return data.cpu().numpy().tolist()

    elif isinstance(data, ndarray):
        return data.tolist()

    raise ValueError("Data should be a Tensor or a numpy array.")
