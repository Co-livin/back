# back

Перед работой с кодом:
``` bash
python -m venv venv
venv\Scripts\activate
```
``` bash
pip install -r requirements.txt
```

Перед коммитом:
``` bash
ruff format
```

## Порты:
Внешние адреса:
> Фронт - http://colivin.ru (порт 443)

> Документация API - https://colivin.ru/api/docs

> pgAdmin -  https://colivin.ru/pgadmin/


Порты в docker-compose:
> 5432 - db

> 8000 - backend

> 80 - pgAdmin

> 80, 443 - nginx

## Ручки 

Cистемные
> GET /health - проверяет, жив ли сервер

Аутентификация (/auth)
> POST /auth/register - регистирует нового пользователя в базе, хэширует пароль

> POST /auth/login - проверяет логин и пароль, выдаёт JWT токен для дальнейшего доступа к сервисам

> GET /auth/me - читает JWT токен и возвращает текущего авторизованного пользователя

Пространства (/spaces)
> POST /spaces/ - создаёт новое пространство, выдаёт инвайт-код и присваивает создателю роль owner

> GET /spaces/my - возвращает список всех простраств, где состоит текущий user

> POST /spaces/join - вступить в пространство по инвайт-коду

> GET /spaces/{space_id}/members - список всех участников пространства и их роли (только для членов пространства)

> DELETE /spaces/{space_id}/members/{user_id} - удаляет участника из пространства (доступно admin и owner)

> PATCH /spaces/{space_id}/members/{user_id}/role - изменяет роль участника

Задачи (/tasks)
> POST /spaces/{space_id}/tasks - создать новую задачу 

> GET /spaces/{space_id}/tasks - список всех активных задач в пространстве

> POST /tasks/{task_id}/complete - отмечает задачу выполненной

Лента (/events)
> GET /spaces/{space_id}/events - история активностей в пространстве в хронологическом порядке

Действия с пользователями (/users)
> GET /users/by-login/{login} - найти юзера по его логину

> GET /users/by-id/{id} - найти юзера по его айди

Все ручки кроме логина/авторизации/health требует JWT токен в заголовке (Authorization: Bearer <токен>)