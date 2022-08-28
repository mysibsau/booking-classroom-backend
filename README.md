# server.backend

Основной модуль бэкенда

## Локальная разработка
1) Создать виртуальное окружение c Python3.10

``virtualenv env -p python3.10``

2) Запустить окружение

``source env/bin/activate``

3) Установть зависимости

``pip install -r requirements.txt``

4) Перейти в папку с проектом

``cd src/``

5) Запустить проект

``uvicorn main:app``

Теперь можно открыть в браузере страницу http://127.0.0.1:8000/docs, где будет представлена документация со всеми реализованными API методами.

## Миграции

1) Миграции хранятся по пути `migrations/versions`
2) Миграции автоматически подтягивают изменения сделанные в моделях, которые хранятся по пути `src/models/` чтобы модель отслеживалась она обязательно должна быть импортирована в `src/models/__inti__.py`
3) Создать новую миграцию можно командой `alembic revision --autogenerate -m "название миграции"`
4) После создания миграцию нужно накатить на бд, командой `alembic upgrade head`
5) Миграции можно и откатывать, для этого используется команда `alembic downgrade -1` вместо -1 пишем число миграций которые надо откатить.

Подробнее: https://alembic.sqlalchemy.org/en/latest/index.html

## Подключение к postgreSQL

1) установить postgreSQL на систему:
   1) sudo apt update
   2) sudo apt install postgresql postgresql-contrib

2) создать пользователя БД с логином из конфигурационного файла:
   1) sudo -u postgres createuser <username>
     
3) создать БД c именем из конфигурационного файла:
   1) sudo -u postgres createdb <dbname>
     
4) перейти в консоль postgreSQL:
   1) sudo -u postgres psql
     
5) задать пароль из конфигурационного файла:
   1) alter user <username> with encrypted password '<password>';
    
6) не выходя из консоли postgreSQL, дать пользователю все права на работу с БД:
   1) grant all privileges on database <dbname> to <username> ;

Подробнее: https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e
