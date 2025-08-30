import pytest
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_db():
    async for db in get_db():
        assert isinstance(db, AsyncSession)
