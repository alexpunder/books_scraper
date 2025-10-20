## Описание проекта.  

_**Парсер сайта с книгами "books.toscrape.com"**_ - скрипт, позволяющий решить следующую задачу: обойти каталог книг,
    извлечь детальную информации о каждой книге и сохраненить результатов. При необходимости, можно создать ежедневную задачу для автоматического парсинга.

## Используемые технологии.

![Python 3.12](https://img.shields.io/badge/Python-3.12-brightgreen.svg?style=flat&logo=python&logoColor=white)
![Pytest 8.4.2](https://img.shields.io/badge/Pytest-Testing-brightgreen?style=flat&logo=pytest)
![Requests 2.32.5](https://img.shields.io/badge/Requests-HTML%20Requests-red?style=flat&logo=python)
![Schedule 1.2.2](https://img.shields.io/badge/Schedule-Task%20Scheduling-blue?style=flat&logo=clockify)

## Установка проекта.  

1. Находясь в дериктории, где будет размещаться проект, склонируйте его репозиторий:  
```
git@github.com:alexpunder/books_scraper.git
```
2. Перейди в папку проекта:  
```
cd books_scraper
```
3. Создай виртуальное окружение, после - активируйте его:  
```
python -m venv venv
```
```
source venv/Scripts/activate
```
4. Установите необходимые для проекта зависимости (*_при необходимости, обновите pip_):
```
python -m pip install --upgrade pip
```
```
pip install -r requierements.txt 
```
5. В файле `constants.py` настройте необходимое время запуска, частоту проверки и другие параметры (при необходимости).

## Пример работы скрипта.

Если установлен флаг сохранения в файл на `True`, то запись о книгах будет иметь вид списка словарей со следующими данными:  
```
[
  {
    "Title": "A Light in the Attic",
    "Price": "£51.77",
    "Available": "22",
    "Rating": "3",
    "Description": "It's hard to imagine a world without A Light in the Attic. This now-classic <...> more",
    "Info_table": {
      "UPC": "a897fe39b1053632",
      "Product Type": "Books",
      "Price (excl. tax)": "£51.77",
      "Price (incl. tax)": "£51.77",
      "Tax": "£0.00",
      "Number of reviews": "0"
    }
  },
  ...
]
```

## Тестирование.

Из корневой директории проекта выполните команду `pytest`. Каждый тест должен завершиться статусом `PASSED`
