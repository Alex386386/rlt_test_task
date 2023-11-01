# Тестовое задание(бот для агрегации данных)

### Описание

Проект представляет собой бота для взаимодействия с базой данных MongoDB и агрегации статических зарплатных данных.

## Stack 

Python 3.11, python-telegram-bot 20.06, MongoDB, Docker, Docker-compose


### Установка, Как запустить проект:
https://github.com/Alex386386/rlt_test_task
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Alex386386/rlt_test_task.git
```

Перейдите в папку с проектом:

```
cd rlt_test_task
```

Cоздайте файл .env со следующим наполнением:

```
TELEGRAM_TOKEN=<your telegram token>
MONGO_HOST=mongo
MONGO_PORT=27017
```


Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Запуск приложения в фоновом режиме:

```
sudo docker compose up -d
```

Автор:
- [Александр Мамонов](https://github.com/Alex386386) 