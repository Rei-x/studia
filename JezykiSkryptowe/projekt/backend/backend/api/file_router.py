import os
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlmodel import desc, select

from backend.api.deps import SessionDep
from backend.models import File, FilePublic, ResponseModel
from backend.agents.rag import process_file_with_unstructured, qdrant_client
from qdrant_client.http import models as rest
from backend.core.config import settings

file_router = APIRouter()


@file_router.get("/files", response_model=list[FilePublic])
async def files(session: SessionDep):
    return session.exec(select(File).order_by(desc(File.created_at)).limit(100)).all()


@file_router.delete("/files/{file_id}", response_model=ResponseModel)
async def delete_file(file_id: str, session: SessionDep):
    file = session.exec(select(File).where(File.id == file_id)).one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file.on_disk)

    session.delete(file)
    qdrant_client.delete(
        "docs",
        points_selector=rest.FilterSelector(
            filter=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="metadata.id", match=rest.MatchValue(value=file_id)
                    )
                ]
            )
        ),
    )
    session.commit()

    return {"message": "File deleted successfully"}


@file_router.post("/upload")
async def upload_file(files: list[UploadFile], session: SessionDep):
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)

    for file in files:
        contents = await file.read()
        file_size = len(contents)

        if not file.filename:
            raise HTTPException(status_code=400, detail="No file name provided")

        random_filename = f"{uuid4()}"
        file_path = f"{settings.UPLOAD_DIR}/{random_filename}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)
        new_file = File(
            id=uuid4().hex,
            filename=file.filename,
            on_disk=file_path,
            size=file_size,
        )
        session.add(new_file)

        if not new_file.id:
            raise HTTPException(status_code=500, detail="Failed to upload file")

        await process_file_with_unstructured(contents, file.filename, id=new_file.id)
        session.commit()

    return {"message": "Files uploaded successfully"}


@file_router.get("/files/{file_id}")
async def get_file(file_id: str, session: SessionDep):
    file = session.exec(select(File).where(File.id == file_id)).one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(
        open(file.on_disk, "rb"), media_type="application/octet-stream"
    )
