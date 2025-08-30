# Task Manager API (Test Case)

Тестовое задание для компании **skycapital.group**.  
Приложение реализовано на *FastAPI* с использованием *SQLAlchemy* и *SQLite*.  

Реализованы CRUD-операции для задач, покрытые тестами (pytest + pytest-asyncio + pytest-cov).

Для удобства присутствует Makefile.

---

## Установка и запуск

:frog: В проекте используется [uv](https://github.com/astral-sh/uv) вместо pip/poetry/pipenv.  
Все команды в `Makefile` завязаны именно на *uv*.  

Для установки зависимостей через pip присутствует `requirements.txt`.

### 1. Сборка проекта
```bash
make build
```

### 2. Запуск сервера
```bash
make run
```

- Приложение доступно по адресу: http://localhost:8000
- Документация OpenAPI: http://localhost:8000/docs

### 3. Запуск тестирования
```bash
make test
```

## Тестирование и покрытие кода (скриншот)

![coverage test](./images/coverage_test.png)