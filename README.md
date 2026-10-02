# network-technologies

Репозиторий в рамках учебной дисциплины "Сетевые технологии"

---
# Технологии

* Git
* Python
* REST API
* FastAPI
* Docker

---
# Возможности

* Создание задачи
* Получение всех задач
* Получение задач по ID
* Обновление задач
* Удаление задач

---
# Как запустить
1. Установить Docker

Скачать:

https://www.docker.com/products/docker-desktop/

После установки запустить Docker Desktop.

---
2. Клонировать проект
```bash
git clone <repository_url>
```
Перейти в папку проекта:
```bash
cd requests-api
```
---
3. Создайте образ
```bash
docker build --rm -t network-technologies .
```
В Linux-системах выполняейте команду от имени root, если не используете rootless docker.

---
4. Создайте контейнер
```bash
docker run --rm --name network-technologies -p 8000:80 network-technologies:latest
```
В Linux-системах выполняейте команду от имени root, если не используете rootless docker.

---
# Примеры запросов:

**Создать задачу (POST /task)**

```bash
curl -X POST 'http://127.0.0.1:8000/task' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "title": "Настроить доступ к базе",
    "description": "Нужно выдать права на чтение для нового аналитика.",
    "status": "new"
  }'
```

**Ожидаемый ответ:**
```json
{"message": "Задача добавлена."}
```
---

**Получить все задачи (GET /task)**

```bash
curl 'http://127.0.0.1:8000/task'
```

**Пример ответа:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Настроить доступ к базе",
      "description": "Нужно выдать права на чтение для нового аналитика.",
      "status": "new"
    },
    {
      "id": 2,
      "title": "Обновить документацию",
      "description": "Актуализировать раздел про авторизацию.",
      "status": "in_progress"
    }
  ]
}
```

---

**Получить одну задачу по ID (GET /task/{task_id})**

```bash
curl 'http://127.0.0.1:8000/task/1'
```

**Если задача есть:**
```json
{
  "task": {
    "id": 1,
    "title": "Настроить доступ к базе",
    "description": "Нужно выдать права на чтение для нового аналитика.",
    "status": "new"
  }
}
```

**Если задачи нет:**
```json
{ "message": "Задачи с таким ID не существует" }
```

---

**Обновить задачу (PUT /task/{task_id})**

```bash
curl -X PUT 'http://127.0.0.1:8000/task/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 3,
    "title": "Закончился картридж в МФУ",
    "description": "В приемной директора принтер МФУ Катюша начал печатать с белыми полосами. Нужна замена картриджа.",
    "status": "new"
  }'
```

**Если успех:**
```json
{
  "message": "Задача обновлена",
  "task": {
    "id": 3,
    "title": "Закончился картридж в МФУ",
    "description": "В приемной директора принтер МФУ Катюша начал печатать с белыми полосами. Нужна замена картриджа.",
    "status": "new"
  }
}
```

**Ошибка, если задачи с таким ID нет:**
```json
{ "message": "Задачи с таким ID не найдена" }
```

---

**Удалить задачу (DELETE /task/{task_id})**

```bash
curl -X DELETE 'http://127.0.0.1:8000/task/2'
```

**Если успех:**
```json
{ "message": "Задача удалена" }
```

**Если записи нет**
```json
{ "massage": "Задачи с таким ID не существует."}
```