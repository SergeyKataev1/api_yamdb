# Учебный проект Яндекс Практикума 'api_yamdb'

----

## Описание api_yamdb
api_yamdb - это учебный проект курса "backend-python" от Яндекс-Практикума, 
где можно добавлять произведения и давать им отзыв с оценкой.
Так же можно комментировать отзывы. Все возможности реализованны через api.

## Возможности api_yamdb
- Регистрация пользователя
- Аутентификация пользователя
- Пользователь может создавать произведение и редактировать
- Пользователь может создавать отзыв и редактировать
- Пользователь может создавать комментарий и редактировать
- У любого пользователя, даже не аутентифицированного, есть возможность 
просматривать произведения, отзывы и комментарии к ним.

## Как развернуть проект

### Нужно в командной строке сделать следующее:
1. Клонировать репозиторий
    ``` 
    git clone https://github.com/DiDiPavlov/api_yamdb.git
    ```
2. Перейти в него
    ```
    cd api_final_yatube
    ```
3. Cоздать виртуальное окружение:
   - Windows
    ```
    python -m venv venv
    ```
   - Linux и macOS
    ```
    python3 -m venv venv
    ```
4. Активировать виртуальное окружение
   - Windows
    ```
    source venv/Scripts/activate
    ```
   - Linux и macOS
    ```
    source venv/bin/activate
    ```
5. Установить зависимости из requirements.txt:
   - Windows
    ```
    pip install -r requirements.txt
    ```
   - Linux и macOS
    ```
    pip install -r requirements.txt
    ```
6. Перейти в папку api_yamdb, где находится manage.py
    ```
    cd api_yamdb
    ```
7. Выполнить миграции
   - Windows
    ```
    python manage.py migrate
    ```
   - Linux и macOS
    ```
    python3 manage.py migrate
    ```
8. Запустить проект
   - Windows
    ```
    python manage.py runserver
    ```
   - Linux и macOS
    ```
    python3 manage.py runserver
    ```
  
## Как загрузить данные для тестирования проекта

1. Из клонированного репозитория скопировать папку /static/data в безопасное место, либо 
использовать для запуска скрипта папку /static/data

2. Перейти в выбранную папку

3. Cоздать виртуальное окружение
   - Windows
   ```
   python -m venv venv
   ```
   - Linux и macOS
    ```
    python3 -m venv venv
    ```
4. Активировать виртуальное окружение
   - Windows
    ```
    source venv/Scripts/activate
    ```
   - Linux и macOS
    ```
    source venv/bin/activate
    ```
5. Установить зависимости из requirements.txt:
   - Windows
    ```
    pip install -r requirements.txt
    ```
   - Linux и macOS
    ```
    pip install -r requirements.txt
    ```
6. Настроить конфигурацию для доступа к данным в файле .env  
Например:
   ```
    # файлы CSV должны находиться в папке, заданной параметром
    DEFAULT_CSV_PATH=./data/
    # файл базы данных db.sqlite3 расположен в папке, заданной параметром
    DEFAULT_SQL_PATH=C:/api_yamdb/api_yamdb/db.sqlite3
    ```
7. Файлы CSV можно дополнять данными, при этом формат и структура должны строго соответствовать образцам, находящимся в папке проекта "static/data"

8. Ознакомиться с режимами запуска скрипта
   - Windows
    ```
    python data_load.py --help
    ```
   - Linux и macOS
    ```
    python3 data_load.py --help
    ```
9. Запустить скрипт для загрузки начальных данных


## Примеры запросов к api_yamdb 
  *(При запущенном проекте вбить в поисковую строку в браузере один из запросов)*
- запрос списка произведений
    ```
    http://127.0.0.1:8000/api/v1/titles/
    ```
- запрос конкретного произведения

    ```
    http://127.0.0.1:8000/api/v1/titles/1/
    ```

- запроc списка отзывов на конкретное произведение

    ```
    http://127.0.0.1:8000/api/v1/titles/1/reviews/
    ```

- запрос комментариев к конкретному отзыву

    ```
    http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/
    ```  

### [Полная документация к запросам](http://127.0.0.1:8000/redoc/)
  
#### ***Тут нужно будет стороннее приложение для работы с api, например Postman***
  
## Авторы работы:
- [Андрей Кумановский](https://github.com/akumanowski)
- [Сергей Катаев](https://github.com/SergeyKataev1)
- [Павлов Дмитрий ](https://github.com/DiDiPavlov)
