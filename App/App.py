import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
client.drop_database("movies_library")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]


def login(name, password):
    user = users_col.find_one({"name": name})
    print(user)
    if not user:
        print("wrong username or password")
        return None
    if user["password"] != password:
        print("wrong username or password")
        return None
    return user["_id"]

print(login("David Gebhard", "2Cbgopm2"))
