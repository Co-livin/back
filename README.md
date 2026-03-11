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
Внешние порты:
> 80 - HTTP Nginx (http://colivin.ru)

> 443 - HTTPS Nginx (https://colivin.ru)

> 8000 - Backed API (https://colivin.ru/docs) 

> 5050 - pgAdmin (https://colivin.ru/pgadmin/)

> 5432 - PostgreSQL

Порты в docker-compose:
> 5432 - db

> 8000 - backend

> 80 - pgAdmin

## Ручки

Cистемные
> GET /health - проверяет, жив ли сервер

Аутентификация
> POST /auth/register - регистирует нового пользователя в базе, хэширует пароль

> POST /auth/login - проверяет логин и пароль, выдаёт JWT токен для дальнейшего доступа к сервисам

> GET /auth/me - читает JWT токен и возвращает текущего авторизированного пользователя
