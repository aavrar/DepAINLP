from typing import Generator

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.model_loader import ModelLoader


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_model_loader(request: Request) -> ModelLoader:
    return request.app.state.model_loader
