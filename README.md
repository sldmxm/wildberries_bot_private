# wildberries_telegram_bot

[![Praktikum](https://yastatic.net/q/logoaas/v2/%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81.svg?circle=black&color=000&first=white)](https://practicum.yandex.ru/profile/backend-developer/) [![Praktikum](https://yastatic.net/q/logoaas/v2/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC.svg?color=000)](https://practicum.yandex.ru/profile/backend-developer/)
команда студентов Яндекс Практикума

## Описание проекта
Телеграм-бот, который помогает узнать позицию товара в выдаче по поисковому запросу.

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

Запустить сервер на локальной машине:
```
python manage.py runserver
```
Админку бота можно посмотреть на странице http://127.0.0.1:8000/admin/
Для тестирования самого бота необходимо создать собственный .env-файл по шаблону .env.example

## Требования к версии Python
Работает на Python 3.11.0