import pytest
from app.schemas import TaskStatus
import app.crud as crud
import app.schemas as schemas
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_task(async_client):
    # Создаем задачу
    response = await async_client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
        },
    )

    # Проверяем ответ
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["status"] == TaskStatus.CREATED.value
    assert "created_at" in data
    assert "updated_at" in data
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


@pytest.mark.asyncio
async def test_get_tasks(async_client):
    # Создаем задачу
    response = await async_client.post("/tasks/", json={"title": "Second"})
    task_id = response.json()["id"]

    # Получаем задачу
    response = await async_client.get(f"/tasks/{task_id}")

    # Проверяем полученную задачу
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Second"


@pytest.mark.asyncio
async def test_get_list_tasks(async_client):
    # Создаем задачи
    await async_client.post("/tasks/", json={"title": "Task 1"})
    await async_client.post("/tasks/", json={"title": "Task 2"})

    # Получаем список задач
    response = await async_client.get("/tasks/?offset=0&limit=10")

    # Проверяем список задач
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_update_task(async_client):
    # Создаем задачу
    response = await async_client.post("/tasks/", json={"title": "Old Title"})
    task_id = response.json()["id"]

    # Обновляем задачу
    response = await async_client.put(
        f"/tasks/{task_id}",
        json={
            "status": TaskStatus.IN_PROGRESS.value,
        },
    )

    # Проверяем обновленную задачу
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Old Title"
    assert data["status"] == TaskStatus.IN_PROGRESS.value
    assert data["updated_at"] is not None


@pytest.mark.asyncio
async def test_delete_task(async_client):
    # Создаем задачу
    response = await async_client.post("/tasks/", json={"title": "To be deleted"})
    task_id = response.json()["id"]

    # Удаляем задачу
    response = await async_client.delete(f"/tasks/{task_id}")

    # Проверяем, что задача удалена
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] is not None

    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] is not None


@pytest.mark.asyncio
async def test_get_nonexistent_task(async_client):
    # Пытаемся получить несуществующую задачу
    response = await async_client.get("/tasks/99999")

    # Проверяем ответ
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] is not None


@pytest.mark.asyncio
async def test_update_nonexistent_task(async_client):
    # Пытаемся обновить несуществующую задачу
    response = await async_client.put(
        "/tasks/99999",
        json={
            "status": TaskStatus.COMPLETED.value,
        },
    )

    # Проверяем ответ
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] is not None


@pytest.mark.asyncio
async def test_delete_nonexistent_task(async_client):
    # Пытаемся удалить несуществующую задачу
    response = await async_client.delete("/tasks/99999")

    # Проверяем ответ
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] is not None


@pytest.mark.asyncio
async def test_create_task_missing_title(async_client):
    # Создаем задачу без заголовка
    response = await async_client.post(
        "/tasks/",
        json={
            "description": "No title -_-",
        },
    )

    # Проверяем ответ
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] is not None


@pytest.mark.asyncio
async def test_get_not_found_from_db(async_session: AsyncSession):
    task = await crud.get_task(async_session, task_id=99999)
    assert task is None


@pytest.mark.asyncio
async def test_get_from_db(async_session: AsyncSession):
    new_task = schemas.TaskCreate(title="Test", description="Desc")
    task = await crud.create_task(async_session, new_task)

    assert task is not None
    assert task.id is not None
    assert task.title == "Test"

    fetched = await crud.get_task(async_session, task.id)
    assert fetched is not None
    assert fetched.id == task.id


@pytest.mark.asyncio
async def test_update_task_from_db(async_session: AsyncSession):
    task = await crud.create_task(
        async_session, schemas.TaskCreate(title="Old", description="Desc")
    )
    assert task is not None

    update = schemas.TaskUpdate(title="New")
    assert update is not None
    updated = await crud.update_task(async_session, task.id, update)
    assert updated is not None

    assert updated.title == "New"


@pytest.mark.asyncio
async def test_update_task_not_found_from_db(async_session: AsyncSession):
    update = schemas.TaskUpdate(title="Ghost")
    result = await crud.update_task(async_session, 999, update)
    assert result is None


@pytest.mark.asyncio
async def test_delete_task_from_db(async_session: AsyncSession):
    task = await crud.create_task(
        async_session, schemas.TaskCreate(title="Del", description="D")
    )
    assert task is not None

    deleted = await crud.delete_task(async_session, task.id)
    assert deleted is not None
    assert deleted.id == task.id

    # Проверяем повторное удаление
    deleted2 = await crud.delete_task(async_session, task.id)
    assert deleted2 is None
