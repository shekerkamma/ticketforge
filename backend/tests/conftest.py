import asyncio
import os
import uuid
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

# Set test env vars BEFORE importing app modules (settings load at import time)
os.environ["DATABASE_URL"] = "sqlite+aiosqlite://"
os.environ["JWT_SECRET"] = "test-secret"

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

# Patch encryption to use a valid Fernet key for tests
import app.services.encryption as _enc_mod
from cryptography.fernet import Fernet as _Fernet
_enc_mod._fernet = _Fernet(_Fernet.generate_key())

from app.api.deps import get_current_user
from app.db import Base, get_session
from app.main import app
from app.models.user import User


# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite://"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


# Fixed UUIDs for test data
TEST_USER_ID = uuid.UUID("00000000000000000000000000000001")
TEST_USER_2_ID = uuid.UUID("00000000000000000000000000000002")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Create all tables before each test, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user in the database."""
    user = User(
        id=TEST_USER_ID,
        github_id=12345,
        github_login="testuser",
        github_access_token="fake-token",
        email="test@example.com",
        avatar_url="https://example.com/avatar.png",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_user_2(db_session: AsyncSession) -> User:
    """Create a second test user."""
    user = User(
        id=TEST_USER_2_ID,
        github_id=67890,
        github_login="testuser2",
        github_access_token="fake-token-2",
        email="test2@example.com",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_client(test_user: User) -> TestClient:
    """TestClient with auth dependency overridden to return test_user."""

    async def _override_get_session():
        async with TestSessionLocal() as session:
            yield session

    async def _override_get_current_user():
        return test_user

    app.dependency_overrides[get_session] = _override_get_session
    app.dependency_overrides[get_current_user] = _override_get_current_user

    client = TestClient(app, raise_server_exceptions=False)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def mock_docker_client():
    client = MagicMock()
    container = MagicMock()
    container.id = "abc123def456"
    container.exec_run.return_value = (0, (b"output", b""))
    container.stop = MagicMock()
    container.remove = MagicMock()
    client.containers.run.return_value = container
    client.containers.get.return_value = container
    return client
