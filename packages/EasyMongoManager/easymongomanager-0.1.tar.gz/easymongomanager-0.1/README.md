# EasyMongoManager

`EasyMongoManager` — это простой интерфейс для взаимодействия с MongoDB с использованием Python.

## Установка

```bash
pip install EasyMongoManager

## Пример использования

from EasyMongoManager import MongoManager

# Создаем подключение к базе данных
db = MongoManager('my_database')

# Вставляем данные
db.insert('my_collection', {'name': 'John', 'age': 30})

# Ищем данные
docs = db.find('my_collection', {'name': 'John'})
print(docs)
