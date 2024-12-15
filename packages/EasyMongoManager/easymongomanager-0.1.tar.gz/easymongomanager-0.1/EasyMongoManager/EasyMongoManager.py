import pymongo
from pymongo.errors import ConnectionFailure, ConfigurationError
import logging

logging.basicConfig(level=logging.INFO)

class MongoManager:
    def __init__(self, db_name: str, username: str = None, password: str = None, ip: str = 'localhost', port: int = 27017):
        try:
            connection_string = (
                f"mongodb://{username}:{password}@{ip}:{port}/"
                if username and password
                else f"mongodb://{ip}:{port}/"
            )
            self.client = pymongo.MongoClient(connection_string)
            self.client.admin.command('ping')  # Проверка подключения
            logging.info('Successful connection to MongoDB!')
        except (ConnectionFailure, ConfigurationError) as e:
            raise SystemExit(f"Error connecting to MongoDB: {e}")

        self.db_name = db_name
        self.db = self.client.get_database(db_name)
        if db_name not in self.client.list_database_names():
            logging.warning(f"The database '{db_name}' does not exist. It will be created upon data insertion.")
        else:
            logging.info(f"Connected to the existing database '{db_name}'.")


    def get_collection(self, collection_name: str):
        """
        Получение коллекции из базы данных.
        """
        return self.db[collection_name]


    def insert(self, collection_name: str, data: dict | list):
        """
        Добавление одного или нескольких документов в коллекцию.

        :param collection_name: Название коллекции.
        :param data: Один документ (dict) или список документов (list[dict]).
        :return: ID вставленных документов.
        """
        collection = self.get_collection(collection_name)
        if isinstance(data, list):
            result = collection.insert_many(data)
            logging.info(f"Inserted {len(result.inserted_ids)} documents.")
            return result.inserted_ids
        elif isinstance(data, dict):
            result = collection.insert_one(data)
            logging.info(f"Inserted document with ID: {result.inserted_id}")
            return result.inserted_id
        else:
            raise ValueError("Data must be a dictionary or a list of dictionaries.")


    def find(self, collection_name: str, query: dict = None, one: bool = False):
        """
        Поиск документов в коллекции.

        :param collection_name: Название коллекции.
        :param query: Условие поиска (dict). По умолчанию — пустой запрос.
        :param one: Если True, возвращается только один документ.
        :return: Найденный документ или список документов.
        """
        collection = self.get_collection(collection_name)
        query = query or {}
        if one:
            document = collection.find_one(query)
            logging.info("Found one document.")
            return document
        else:
            documents = list(collection.find(query))
            logging.info(f"Found {len(documents)} documents.")
            return documents


    def update(self, collection_name: str, query: dict, update_data: dict, many: bool = False):
        """
        Обновление документов в коллекции.

        :param collection_name: Название коллекции.
        :param query: Условие поиска (dict).
        :param update_data: Данные для обновления (dict).
        :param many: Если True, обновляются все подходящие документы. Иначе — один.
        :return: Результат обновления (matched_count, modified_count).
        """
        collection = self.get_collection(collection_name)
        if many:
            result = collection.update_many(query, {'$set': update_data})
            logging.info(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
        else:
            result = collection.update_one(query, {'$set': update_data})
            logging.info(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
        return result.matched_count, result.modified_count

    def delete(self, collection_name: str, query: dict, many: bool = False):
        """
        Удаление документов из коллекции.

        :param collection_name: Название коллекции.
        :param query: Условие поиска (dict).
        :param many: Если True, удаляются все подходящие документы. Иначе — один.
        :return: Количество удаленных документов.
        """
        collection = self.get_collection(collection_name)
        if many:
            result = collection.delete_many(query)
            logging.info(f"Deleted {result.deleted_count} documents.")
        else:
            result = collection.delete_one(query)
            logging.info(f"Deleted {result.deleted_count} document(s).")
        return result.deleted_count

    def close_connection(self):
        """
        Закрытие соединения с MongoDB.
        """
        self.client.close()
        logging.info("Connection to MongoDB closed.")