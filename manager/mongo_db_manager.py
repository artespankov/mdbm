import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo import ReturnDocument

class MongoDBManager:
    HOST_DOMAIN = 'localhost'
    HOST_PORT = 27017

    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)
        self.db_name = db_name
        self.db = self.client[db_name]
        self.__table = None

        self.exceptions = {"db_connect": "DB connection is required for this action.",
                           "table_set": "Table identifier must be set.",
                           "table_query": "Table must be identified before it can be queried.",
                           "obj_serialize": "Object cannot be serialized.",
                           "obj_create_bulk": "Objects dataset must be the list of dictionaries."}

    def __get_collection(self, name):
        """
        Get Collection by name
        Collection is a group of Documents (DB entries)
        and can be threaten as 'table' in regular RDBS
        :return: Collection
        """
        if self.db:
            collection = self.db[name]
        else:
            raise Exception(self.exceptions.get("db_connect"))
        return collection

    def __doc_id(self, object_id):
        if not isinstance(object_id, ObjectId):
            object_id = ObjectId(object_id)
        return object_id

    def __find(self, params, limit=None):
        if self.__table:
            if limit:
                cursor = self.__table.find(params, limit=limit)
            else:
                cursor = self.__table.find(params)
            return cursor
        else:
            raise Exception(self.exceptions.get("table_query"))

    def serialize_object(self, obj):
        """
        Representation of object suitable for saving to db
        :return: serialized object (json representation)
        """
        try:
            serialized_obj = json.dumps(obj)
            return serialized_obj
        except json.JSONDecodeError:
            raise Exception(self.exceptions.get("db_connect"))

    def list_tables(self):
        if self.db:
            return self.db.collection_names(include_system_collections=False)
        else:
            raise Exception(self.exceptions.get("db_connect"))

    def set_table(self, name):
        """
        Set current working Collection
        :param name:
        :return:
        """
        if name:
            self.__table = self.__get_collection(name)
            return self.__table
        else:
            raise Exception(self.exceptions.get("table_set"))

    def create(self, data):
        """
        Insert new Document to existing Collection
        :param data: dictionary with object's data
        :return: ObjectId of added object
        """
        if self.__table:
            object_id = self.__table.insert_one(data).inserted_id
            return object_id
        else:
            raise Exception(self.exceptions.get("table_query"))

    def create_bulk(self, data_list):
        """
        Add one or more Documents to existing Collection
        :param data_list: list of dictionaries with objects data
        :return: list of ObjectId items
        """
        if not isinstance(data_list, list):
            raise Exception(self.exceptions.get("table_query"))
        if self.__table:
            result = self.__table.insert_many(data_list)
            return result.inserted_ids
        raise Exception(self.exceptions.get("table_query"))

    def update(self, filter_set, alter_set):
        """
        Update one document matched by set of fields
        :param filter_set: dict with lookup Document's fields
        :param alter_set: dict with Document's fields-values to be updated
        :return:
        """
        result = self.__table.find_one_and_update(
            filter_set,
            {'$set': alter_set},
            return_document=ReturnDocument.AFTER)
        return result

    def update_by_id(self, obj_id, alter_set):
        """
        Update one Document matched by identifier
        :param obj_id: Document identifier
        :param alter_set: dict with Document's fields-values to be updated
        :return:
        """
        result = self.update(
            filter_set={'_id': obj_id},
            alter_set=alter_set)
        return result

    def update_bulk(self, filter_set, alter_set):
        """
        :param filter_set: dict with lookup Document's fields
        :param alter_set: dict with Document's fields-values to be updated
        :return: Count of updated Documents
        """
        result = self.__table.update_many(
            filter_set, 
            {'$set': alter_set}
        )
        return result.modified_count

    def get_by_id(self, obj_id):
        """
        Find data for one Document by id
        :param obj_id: id of object - int/string/ObjectId
        :return: dict with Document's data
        """
        # ensure the id of object is the instance of specific type - ObjectId
        doc_id = self.__doc_id(obj_id)
        if self.__table:
            return self.__table.find_one({"_id": doc_id})
        else:
            raise Exception(self.exceptions.get("table_query"))

    def get(self, filter_set):
        """
        Get data for one Document by parameters (if there are few objects matched - first one will be returned)
        :param filter_set: dict of filtration parameters
        :return: dict with Document's data
        """
        if self.__table:
            return self.__table.find_one(filter_set)
        else:
            raise Exception(self.exceptions.get("table_query"))

    def filter(self, filter_set, max_amount=None, count_only=False):
        """
        Get list of Documents by parameters
        :param filter_set: dict of filtration parameters
        :param max_amount: limitation for returned objects count (optional)
        :param count_only: return count of matched Documents (without Documents dataset)
        :return: list of dicts with data for matched entries
        """
        results = self.__find(filter_set, max_amount)
        if count_only:
            return results.count()
        return list(results)

    def delete(self, filter_set):
        result = self.__table.delete_many(filter_set)
        return result.deleted_count

    def count(self, filter_set):
        """
        Return amount of Documents in Collection (to match a specific query, pass filtering kwargs)
        :param filter_set: Params to filter counting query
        :return:
        """
        return self.delete(filter_set)

    def __clear_table(self):
        """
        Delete all Documents from active Collection
        :return: Count of deleted Documents
        """
        return self.delete({})

    # def clear(self):
    #     return self.__clear_table()




