# wildberries_telegram_bot

## Описание проекта
Телеграм-бот для определения позиций карточек товаров по ключевым словам на платформе Wildberries. Можно вводить ключевые слова и товары, проверять позиции товаров. Предусмотрена возможность настройки периодической проверки позиций товаров (ежедневно, еженедельно, ежемесячно), а так же экспорта данных в разных форматах.

## Использованные технологии
- django==4.2.2
- python-telegram-bot==20.3

## Инструкции по запуску
Клонировать репозиторий и перейти в него в командной строке:

```
git clone
```

```
cd wildberries_bot_team_1/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в папку, где находится manage.py
```
cd tgbot/
```

Выполнить миграции базы данных
```
python manage.py makemigrations
python manage.py migrate
```

Добавить данные в базу данных данные по умолчанию
```
python manage.py import_data_from_csv
```

Запустить сервер на локальной машине:
```
python manage.py runserver
```
Админку бота можно посмотреть на странице http://127.0.0.1:8000/admin/
Для тестирования самого бота необходимо создать собственный .env-файл по шаблону .env.example

Для использования прокси нужно добавить информацию в .env файл в таком формате:
```dotenv
HTTPS_PROXY='https://USER:PASSWORD@PROXY_IP:PROXY_PORT'
HTTP_PROXY='http://USER:PASSWORD@PROXY_IP:PROXY_PORT'
```

## Требования к версии Python
Работает на Python 3.11.0
