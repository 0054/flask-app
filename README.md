# Flask-app

## подготовка окружения
```
$ virtualenv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

## Запуск тестов
через docker:
```
make run-tests
```
руками:  
запускаем flask app
```
FLASK_ENV=development FLASK_DEBUG=True python3 app.py
```
в другом терминале:
```
pytest
```

## Сборка образа
```
make build
```

## Запуск приложения
```
make start-app
```

## Остановка приложения
```
make stop-app
```
