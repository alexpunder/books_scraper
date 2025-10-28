## Описание проекта.  

_**Парсер книжного сайта "books.toscrape.com"**_

Проект представляет собой скрипт для парсинга каталога книг с сайта "books.toscrape.com". Скрипт извлекает детальную информацию о каждой книге и сохраняет результаты в удобном формате с возможностью автоматизации процесса.

- Парсинг всего каталога книг
- Извлечение полной информации о каждой книге
- Сохранение данных в JSON формате
- Автоматизация парсинга по расписанию
- Тесты

## Используемые технологии.

![Python 3.12](https://img.shields.io/badge/Python-3.12-brightgreen.svg?style=flat&logo=python&logoColor=white)
![Pytest 8.4.2](https://img.shields.io/badge/Pytest-Testing-brightgreen?style=flat&logo=pytest)
![Requests 2.32.5](https://img.shields.io/badge/Requests-HTML%20Requests-red?style=flat&logo=python)
![BeautifulSoup](https://img.shields.io/badge/Beautiful_Soup-4.12.3-orange?style=flat&logo=beautifulsoup)
![Schedule 1.2.2](https://img.shields.io/badge/Schedule-Task%20Scheduling-blue?style=flat&logo=clockify)

- Парсинг: Использует библиотеку `Requests` для HTTP-запросов + `BeautifulSoup` для работы с HTML
- Планирование: `Schedule` для настройки периодического выполнения
- Тестирование: `Pytest` для тестирования

## Установка проекта.  

1. Находясь в дериктории, где будет размещаться проект, склонируйте его репозиторий:  
```
git@github.com:alexpunder/books_scraper.git
cd books_scraper
```
2. Создай виртуальное окружение, после - активируйте его:  
```
python -m venv venv

# Для Windows:
source venv/Scripts/activate
# Для Linux/Mac:
source venv/bin/activate
```
3. Установите необходимые для проекта зависимости (*_при необходимости, обновите pip_):
```
pip install -r requierements.txt 
python -m pip install --upgrade pip
```
4. В файле `constants.py` настройте необходимое время запуска, частоту проверки и другие параметры (при необходимости).

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

## Запуск проекта.  

Для этого достаточно из корневой папки проекта `/books_scraper` в терминале выполнить команду `python3 src/scraper.py`. По умолчанию, скрипт запустится в указанное в переменной `TASK_START_TIME` время и будет сохранять обновленные данные в текстовый файл до тех пор, пока пользователь не прервет его выполнение комбинацией `Ctrl+C`.

## Тестирование.

Из корневой директории проекта выполните команду `pytest`. Каждый тест должен завершиться статусом `PASSED`




