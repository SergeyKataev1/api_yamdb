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
3. Создать виртуальное окружение:
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
1. Перейти в папку api_yamdb/static/data
2. В папке находится скрипт data_load.py и набор файлов CSV. Вы можете дополнить файлы
данными, при этом не меняя названия столбцов.
3. Запустить скрипт:
   - Windows 
    ``` 
    python data_load.py
    ``` 
   - Linux и macOS 
    ``` 
    python3 data_load.py
    ``` 

## Примеры запросов к api_yamdb 
  *(запустить проект, перейти по ссылке **ниже**)*
- запрос списка категория  
[http://127.0.0.1:8000/api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/)
- запрос списка жанров  
[http://127.0.0.1:8000/api/v1/genres/](http://127.0.0.1:8000/api/v1/genres/)
- запрос списка произведений  
[http://127.0.0.1:8000/api/v1/titles/](http://127.0.0.1:8000/api/v1/titles/)
- запрос конкретного произведения  
[http://127.0.0.1:8000/api/v1/titles/1/](http://127.0.0.1:8000/api/v1/titles/1/)
- запрос списка отзывов на конкретное произведение  
[http://127.0.0.1:8000/api/v1/titles/1/reviews/](http://127.0.0.1:8000/api/v1/titles/1/reviews/)
- запрос комментариев к конкретному отзыву  
[http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/](http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/)


## Полная документация к запросам
Запустить проект, перейти по ссылке
[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Использованные в проекте технологии
 - Python 3.9
 - Django 3.2
 - DRF 3.12.4
 - PyJWT 2.1.0
  
## Авторы работы:
- [Андрей Кумановский](https://github.com/akumanowski)
- [Сергей Катаев](https://github.com/SergeyKataev1)
- [Павлов Дмитрий ](https://github.com/DiDiPavlov)
