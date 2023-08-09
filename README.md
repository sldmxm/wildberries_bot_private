# wildberries_telegram_bot

## Описание проекта

Телеграм-бот для определения позиций карточек товаров по ключевым словам на платформе Wildberries. Можно вводить ключевые слова и товары, проверять позиции товаров. Предусмотрена возможность настройки периодической проверки позиций товаров (ежедневно, еженедельно, ежемесячно), а так же экспорта данных в разных форматах.


### Используемые технологии
- :snake: Python 3.11.0
- :incoming_envelope: python-telegram-bot 20.3
- :package: Django 4.2.2



### Как запустить проект на локальной машине:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Studio-Yandex-Practicum/wildberries_bot_team_1.git
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

Перед запуском проекта необходимо создать телеграм канал и чат бот. Добавьте бота в ваш телеграм канал в качестве админа. После чего заполните .env файл по образцу:

```
SECRET_KEY="5sr_o164-b_h3^$bg4pl8pfk7xbd3#=(oul8s@u&4m4bbn*7y%"
CSRF_TRUSTED="127.0.0.1"
TELEGRAM_TOKEN= "5608055777:AAG58ek3skKH45dn34oQOWUPIBVxjWP3Xqз"  # получите токен для бота в @BotFather
CHANNEL_USERNAME="@your_test_channel"  # ссылка на ваш телеграм канал
```

Убедитесь, что в файле tgbot/tgbot/settings.py установлены настройки базы данных:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Перейти в папку, где находится manage.py
```
cd tgbot/
```

Выполнить миграции базы данных
```
python manage.py makemigrations
python manage.py migrate
# В случае возникновения ошибок используйте команду
python manage.py migrate --run-syncdb
```

Добавить данные в базу данных данные по умолчанию
```
python manage.py import_data_from_csv
```

Запустить сервер на локальной машине:
```
python manage.py runserver
```

Откройте новый терминал и запустите бота:
```
python manage.py bot
```
После запуска сервиса перейдите в ваш телеграм бот. Функционал будет доступен после нажатия на кнопку "Меню" в левом нижнем углу интерфейса.

Админку бота можно посмотреть на странице http://127.0.0.1:8000/admin/
Для этого перейдите в терминал и создайте пользователя администратора:

```
python manage.py createsuperuser
```

Для использования прокси нужно добавить информацию в .env файл в таком формате:
```dotenv
HTTPS_PROXY='https://USER:PASSWORD@PROXY_IP:PROXY_PORT'
HTTP_PROXY='http://USER:PASSWORD@PROXY_IP:PROXY_PORT'
```


### Использование рассылки сообщений
Для использования рассылки **не** через docker, необходимо установить redis:
- MacOS
  ```commandline
  brew install redis
  ```
- Linux
  ```commandline
  sudo apt-get install redis
  ```
- Windows

  > не поддерживается Windows, необходимо использовать [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
  и запускать как на linux

После запускаем сервер redis:
```commandline
sudo redis-server
```
Для работы celery в settings.py необходимо добавить
```python
CELERY_BROKER_URL = "redis://localhost:6379"
```
Затем запускаем celery из папки _tgbot/_
```commandline
celery -A tgbot worker
```

## Запуск через Docker (предпочтительный вариант запуска программы)
> При использовании Docker compose не надо устанавливать и запускать сервера redis
(не поддерживается Windows, поэтому необходимо использовать [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install))
и celery.

Убедитесь, что в файле tgbot/tgbot/settings.py установлены настройки базы данных:

```
DATABASES = {
   'default': {
       'ENGINE': os.getenv('DB_ENGINE',
                           default='django.db.backends.postgresql_psycopg2'),
       'NAME': os.getenv('DB_NAME', default='postgres'),
       'USER': os.getenv('POSTGRES_USER', default='postgres'),
       'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
       'HOST': os.getenv('DB_HOST', default='127.0.0.1'),
       'PORT': os.getenv('DB_PORT', default='5432')
   }
}
```

Перед запуском необходимо создать `.env` файл и заполнить его по примеру `.env.example`:
```commandline
touch .env
nano .env
```
Для запуска программы через docker compose необходимо ввести команду:
```commandline
docker compose up --build
```
При первом запуске контейнера необходимо создать, выполнить миграции и собрать статику:
```commandline
docker compose exec -T web python manage.py makemigrations bot
docker compose exec -T web python manage.py makemigrations botmanager
docker compose exec -T web python manage.py makemigrations parser
docker compose exec -T web python manage.py makemigrations users
docker compose exec -T web python manage.py migrate
docker compose exec -T web python manage.py collectstatic --no-input
```
Создать суперпользователя можно командой:
```commandline
docker compose exec -T web python manage.py superuser
```
> login - admin
>
> password - admin


## Тестирование блокировки парсера серверами WB
Существует ненулевая вероятность блокировки со стороны WB запросов парсера по IP.
Протестировать серию запросов:
```commandline
python tgbot/manage.py test parser
```

По умолчанию тест делает серии 250-500-1000 запросов с паузой между ними в 1 час.
Параметры теста находятся в ```tgbot/parser/tests/test_position_parser.py``` в константах ```SERIES_REQUESTS``` и ```SERIES_REQUESTS_PAUSE```.



