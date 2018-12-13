# pymdbm
MongoDB manager toolset based on pymongo

### Pre-requests
* Install and run MongoDB on you OS.
Detailed guide:
https://docs.mongodb.com/manual/administration/install-community/
* Install python3.6+ and setup new virtualenv
* Install dependencies from requirements.txt `pip install -r requirements.txt`

### Examples

```python
import datetime
from manager.mongo_db_manager import MongoDBManager
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

# >>> Current table name:  Superheroes



# List tables in database
print("List of existing tables: ", mdbm.list_tables())

# >>> List of existing tables:  ['Superheroes']



# Insert object
obj_id = mdbm.create(hero)
print("Added object. ID: ", obj_id)

# >>> Added object. ID:  5c124b5ffc4fbae3b73eddaa



# Insert few objects
obj_ids = mdbm.create_bulk(heroes)
print("Added few objects. IDs: ", obj_ids)

# >>> Added few objects. IDs:  [ObjectId('5c124b5ffc4fbae3b73eddab'), ObjectId('5c124b5ffc4fbae3b73eddac')]



# Get object
obj_data = mdbm.get(filter_query)
print("Get object by query: ", obj_data)

# >>> Get object by query:  {'_id': ObjectId('5c124b5ffc4fbae3b73eddaa'), 'nickname': 'Batman', 'alter_ego': 'Bruce Wayne', 
# 'race': 'Earthling', 'occupation': ['Superhero', 'Millionaire', 'Playboy'], 'date': datetime.datetime(1981, 10, 10, 0, 0)}



# Get object by id
obj_data = mdbm.get_by_id(obj_id)
print("Get object by ID:", obj_data)

# >>> Get object by ID: {'_id': ObjectId('5c124b5ffc4fbae3b73eddaa'), 'nickname': 'Batman', 'alter_ego': 'Bruce Wayne', 
# 'race': 'Earthling', 'occupation': ['Superhero', 'Millionaire', 'Playboy'], 'date': datetime.datetime(1981, 10, 10, 0, 0)}



# Get objects
obj_list = mdbm.filter(filter_query)
print("Found {} object(s): {}".format(len(obj_list), obj_list))

# >>> Found 1 object(s): [{'_id': ObjectId('5c124b5ffc4fbae3b73eddaa'), 'nickname': 'Batman', 'alter_ego': 'Bruce Wayne', 
# 'race': 'Earthling', 'occupation': ['Superhero', 'Millionaire', 'Playboy'], 'date': datetime.datetime(1981, 10, 10, 0, 0)}]


limitation = 2
obj_list = mdbm.filter(filter_query, max_amount=limitation)
print("Found {} (with limitation to {}) objects: {}".format(len(obj_list), limitation, obj_list))

# >>> Found 1 (with limitation to 2) objects: [{'_id': ObjectId('5c124b5ffc4fbae3b73eddaa'), 'nickname': 'Batman',
# 'alter_ego': 'Bruce Wayne', 'race': 'Earthling', 'occupation': ['Superhero', 'Millionaire', 'Playboy'], 'date': 
# datetime.datetime(1981, 10, 10, 0, 0)}]



obj_count = mdbm.filter(filter_query, count_only=True)
print("Total count of matched objects:".format(obj_count))

# >>> Total count of matched objects: 1



# Update single object by id
obj_data_modified = mdbm.update_by_id(
    obj_id=obj_id,
    alter_set={"occupation": "Startup-er"}
)
print("Modified object with dataset: {}".format(obj_data_modified))

# >>> Modified object with dataset: {'_id': ObjectId('5c125371fc4fbafdd9d1d606'), 'nickname': 'Batman', 'alter_ego': 
# 'Bruce Wayne', 'race': 'Earthling', 'occupation': 'Startup-er', 'date': datetime.datetime(1981, 10, 10, 0, 0)}



# Update single object by query
obj_data_modified_ = mdbm.update(
    filter_set={"occupation": "Startup-er"},
    alter_set={"occupation": "Unemployed"}
)
print("Modified object with dataset: {}".format(obj_data_modified_))

# >>> Modified object with dataset: {'_id': ObjectId('5c125371fc4fbafdd9d1d606'), 'nickname': 'Batman', 'alter_ego': 
# 'Bruce Wayne', 'race': 'Earthling', 'occupation': 'Unemployed', 'date': datetime.datetime(1981, 10, 10, 0, 0)}



# Update few objects by query
obj_count_modified = mdbm.update_bulk(
    filter_set=filter_query,
    alter_set=modification_data
)
obj_list = mdbm.filter(filter_set=filter_query_modified)
print("Modified {} object(s). Objects list: {}".format(obj_count_modified, obj_list))

# >>> Modified 1 object(s). Objects list: [{'_id': ObjectId('5c124b5ffc4fbae3b73eddaa'), 'nickname': 'Joker', 'alter_ego':
# 'unknown', 'race': 'Earthling', 'occupation': 'Supervillain', 'date': 'unknown'}]



# Delete objects
obj_count_deleted = mdbm.delete(filter_set=filter_query_modified)
print("Delete {} object(s).".format(obj_count_modified, obj_list))

# >>> Deleted 1 object(s).



# Count objects
amount = mdbm.count(filter_set={"nickname": "Aquaman"})
print("Count objects by query:", amount)

# >>> Count objects by query: 1

```
