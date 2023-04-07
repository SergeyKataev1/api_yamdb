# Учебный проект Яндекс Практикума 'api_yamdb'
<details><summary>Описание api_yamdb</summary>
<ul>
api_yamdb - это учебный проект курса "backend-python" от Яндекс-Практикума где можно добавлять произведения и давать им отзыв с оценкой.
Так же можно коментриовать отзывы. Все возможности реализованны через api
</details>
  
<details><summary>Возможности api_yamdb</summary>
<ul>
  <li>Регистрация пользователя</li>
  <li>Аунтетификация пользователя</li>
  <li>Пользоваетель может создавать произведене и реадактировать</li>
  <li>Пользоваетель может создавать отзыв и редактировать</li>
  <li>Пользоваетель может создавать коментарий и редактировать</li>
  <li>У люого пользователя даже не аутентифицированного есть возможность просмотра произвидений, отзывов и коментриев</li>
</ul>  
</details>
  
<details><summary>Как развернуть проект</summary>
  
#### Нужно в командной стоке сделать следуюющее
#### 1 Клонировать репозитарий
``` 
git clone https://github.com/DiDiPavlov/api_final_yatube.git 
```
#### 2 Перейти в него
```
cd api_final_yatube
```
#### 3 Cоздать виртуальное окружение
Windows
```
python -m venv venv
```
Linux и macOS
```
python3 -m venv venv
```
#### 4 Активировать виртуальное окружение
Windows
```
source venv/Scripts/activate
```
Linux и macOS
```
source venv/bin/activate
```
#### 5 Установить зависимости из requirements.txt:
Windows
```
pip install -r requirements.txt
```
Linux и macOS
```
pip install -r requirements.txt
```
#### 6 Перейти в папку api_yamdb где находтися manage.py
```
cd api_yamdb
```
#### 7 Выполнить миграции
Windows
```
python manage.py migrate
```
Linux и macOS
```
python3 manage.py migrate
```
#### 8 Запустить проект
Windows
```
python manage.py runserver
```
Linux и macOS
```
python3 manage.py runserver
```
  
</details>
  
<details><summary>Примеры запросов к api_yamdb </summary> 
  *(При запущенном проекте вбить в поисковую строку в браузере один из запросов)*
<details><summary>запрос произведений</summary>

```
http://127.0.0.1:8000/api/v1/titles/
```
</details>
<details><summary>запрос конкретного произведения</summary>

```
http://127.0.0.1:8000/api/v1/titles/1/
```
</details>

<details><summary>запроc отзывов</summary>

```
http://127.0.0.1:8000/api/v1/titles/1/reviews/
```
</details>

<details><summary>запрос к конкретариев к конкретному отзыву</summary>

```
http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/
```  

</details>
</details>
  
Полня документация к запросам по адрессу  http://127.0.0.1:8000/redoc/
  
*Тут нужно будет сторонее приложение работы с api например Postman*
  
### Автор работы Сергей Катаев, Андрей Кумановский ,Палов Дмитрий

При содейтвии и поддержке наставников и ревьюера Яндекс Практикума




