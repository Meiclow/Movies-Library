import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
client.drop_database("movies_library")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]