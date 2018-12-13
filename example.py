import datetime
from manager.mongo_db_manager import MongoDBManager


if __name__ == '__main__':

    hero = {"nickname": "Batman",
            "alter_ego": "Bruce Wayne",
            "race": "Earthling",
            "occupation": ["Superhero", "Millionaire", "Playboy"],
            "date": datetime.datetime(1981, 10, 10, 0, 0)}

    heroes = [

        {"nickname": "Superman",
         "alter_ego": ["Kal-El", "Clark Kent"],
         "race": "Kryptonian",
         "date": datetime.datetime(1958, 6, 10, 0, 0),
         "occupation": "Superhero"
         },

        {"nickname": "Aquaman",
         "alter_ego": "Arthur Curry",
         "race": "Atlantean",
         "date": datetime.datetime(1975, 8, 20, 0, 0),
         "occupation": "Trident-trivet"}
    ]

    filter_query = {"nickname": "Batman",
                    "date": datetime.datetime(1981, 10, 10, 0, 0)}

    modification_data = {"nickname": "Joker",
                         "alter_ego": "unknown",
                         "occupation": "Supervillain",
                         "date": "unknown"}

    filter_query_modified = {"nickname": "Joker"}

    mdbm = MongoDBManager(host=MongoDBManager.HOST_DOMAIN,
                          port=MongoDBManager.HOST_PORT,
                          db_name='default')

    # Choose table to work with
    table = mdbm.set_table(name="Superheroes")
    print("Current table name: ", table.name)

    # List tables in database
    print("List of existing tables: ", mdbm.list_tables())

    # Insert object
    obj_id = mdbm.create(hero)
    print("Added object. ID: ", obj_id)

    # Insert few objects
    obj_ids = mdbm.create_bulk(heroes)
    print("Added few objects. IDs: ", obj_ids)

    # Get object
    obj_data = mdbm.get(filter_query)
    print("Get object by query: ", obj_data)

    # Get object by id
    obj_data = mdbm.get_by_id(obj_id)
    print("Get object by ID:", obj_data)

    # Get objects
    obj_list = mdbm.filter(filter_query)
    print("Found {} object(s): {}".format(len(obj_list), obj_list))

    limitation = 2
    obj_list = mdbm.filter(filter_query, max_amount=limitation)
    print("Found {} (with limitation to {}) objects: {}".format(len(obj_list), limitation, obj_list))

    obj_count = mdbm.filter(filter_query, count_only=True)
    print("Total count of matched objects: {}".format(obj_count))

    # Update single object by id
    obj_data_modified = mdbm.update_by_id(
        obj_id=obj_id,
        alter_set={"occupation": "Startup-er"}
    )
    print("Modified {} object(s) with dataset: {}".format(len(obj_data_modified), obj_data_modified))

    # Update single object by query
    obj_data_modified_ = mdbm.update(
        filter_set={"occupation": "Startup-er"},
        alter_set={"occupation": "Unemployed"}
    )
    print("Modified {} object(s) with dataset: {}".format(len(obj_data_modified_), obj_data_modified_))

    # Update few objects by query
    obj_count_modified = mdbm.update_bulk(
        filter_set=filter_query,
        alter_set=modification_data
    )
    obj_list = mdbm.filter(filter_set=filter_query_modified)
    print("Modified {} object(s). Objects list: {}".format(obj_count_modified, obj_list))

    # Delete objects
    obj_count_deleted = mdbm.delete(filter_set=filter_query_modified)
    print("Deleted {} object(s).".format(obj_count_modified, obj_list))

    # Count objects
    amount = mdbm.count(filter_set={"nickname": "Aquaman"})

    print("Count objects by query:", amount)
