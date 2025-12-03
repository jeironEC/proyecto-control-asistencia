import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from main import app
from database.session import obtener_db
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

engine_test = create_engine(DATABASE_URL_TEST)

SQLModel.metadata.create_all(bind=engine_test)

@pytest.fixture()
def session():
    with Session(engine_test) as session:
        with session.begin():
            yield session
            session.rollback()
    
@pytest.fixture()
def client(session):
    def obtener_db_():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[obtener_db] = obtener_db_
    with TestClient(app) as c:
        yield c