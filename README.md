# Описание:
Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
### Стек используемых технологий:
- [Python 3.8](https://python.org)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
***
# Как запустить проект:
##### Для Windows:
```python
python
```
##### Для Linux и MacOS:
```python
python3
```
### Клонировать репозиторий и перейти в него в командной строке:
```python
https://github.com/sonyaleontyeva/api_yamdb.git
cd api_yamdb
```
### Cоздать и активировать виртуальное окружение:
```python
python3 -m venv venv
source venv/bin/activate
```
### Обновить пакетный менеджер pip:
```python
python3 -m pip install --upgrade pip
```
### Установить зависимости из файла requirements.txt
```python
pip install -r requirements.txt
```
### Выполнить миграции:
```python
cd api_yamdb
python3 manage.py migrate
```
### Запустить проект:
```python
python3 manage.py runserver
```

#### Полная документация доступна по адресу:
```python
http://127.0.0.1:8000/redoc/
```

## Авторы:
### Антон Сидоров
- отзывы,
- комментарии,
- рейтинг произведений
### Антон Земцов
- Cистема регистрации и аутентификации
- Права доступа
- Работа с токеном
- Система подтверждения через e-mail
- Произведения
- Категории
- Жанры
- Импорт данных из csv файлов
