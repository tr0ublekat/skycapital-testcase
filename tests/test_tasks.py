from httpx import ASGITransport, AsyncClient
import pytest
from app.schemas import TaskStatus
from app.main import app


@pytest.mark.asyncio
async def test_test():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")
    assert response.status_code == 200


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
