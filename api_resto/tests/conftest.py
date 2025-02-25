import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_resto.dependencies.database import Base, get_db
from api_resto.main import app
from api_resto.tests.test_config import TestConfig
from urllib.parse import quote_plus


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{TestConfig.db_user}:{quote_plus(TestConfig.db_password)}@{TestConfig.db_host}:{TestConfig.db_port}/{TestConfig.db_name}?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():

    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    yield
 
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
