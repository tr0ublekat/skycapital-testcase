from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import database, models
from .routers import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan для создания таблиц при старте приложения."""

    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(
    title="Тестовое задание для skycapital.group", version="1.0.0", lifespan=lifespan
)

app.include_router(task_router)
