from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def get_tasks(db: AsyncSession, offset: int = 0, limit: int = 100):
    """Получение всех задач."""

    result = await db.execute(select(models.Task).offset(offset).limit(limit))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int):
    """Получение задачи по ID."""

    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    return result.scalar_one_or_none()


async def create_task(db: AsyncSession, task: schemas.TaskCreate):
    """Создание новой задачи."""

    db_task = models.Task(title=task.title, description=task.description)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id: int, task: schemas.TaskUpdate):
    """Обновление задачи по ID."""

    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    # Обновление полей задачи исключая дефолтные значения
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int):
    """Удаление задачи по ID."""

    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    await db.delete(db_task)
    await db.commit()
    return db_task
