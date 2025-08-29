from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas, database


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[schemas.TaskOut])
async def get_tasks(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(database.get_db),
):
    """Получение всех задач с пагинацией."""

    tasks = await crud.get_tasks(db, offset=offset, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=schemas.TaskOut)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(database.get_db),
):
    """Получение задачи по ID."""

    task = await crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.post("/", response_model=schemas.TaskOut, status_code=201)
async def create_task(
    task: schemas.TaskCreate,
    db: AsyncSession = Depends(database.get_db),
):
    """Создание новой задачи."""

    db_task = await crud.create_task(db, task=task)
    return db_task


@router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    """Обновление задачи по ID."""

    db_task = await crud.update_task(db, task_id=task_id, task=task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return db_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(database.get_db),
):
    """Удаление задачи по ID."""

    db_task = await crud.delete_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"detail": f"Задача с id={task_id} была успешно удалена"}
