import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]


def show_all_objects(collection):
    return collection.find()


def get_id_of_object(name, collection):
    a = collection.find({"name": name}, {"_id": 1})
    for bla in a:
        return bla['_id']


def get_name_of_object(object_id, collection):
    a = collection.find({"_id": object_id}, {"name": 1, "_id": 0})
    for bla in a:
        return bla['name']


def find_object_by_name(name, collection):
    return collection.find({"name": name})


def find_movie_by_year(year, collection):
    return collection.find({"year": year})


def find_movie_by_year_margin(year_from, year_to, collection):
    return collection.find({"$and": [{"year": {"$gte": year_from}}, {"year": {"$lte": year_to}}]})


def find_movie_by_rating(rating, collection):
    return collection.find({"rating": rating})


def find_movie_by_rating_margin(rating_from, rating_to, collection):
    return collection.find({"$and": [{"rating": {"$gte": rating_from}}, {"rating": {"$lte": rating_to}}]})


def find_movie_by_director(director, collection):
    return collection.find({"director": director})


def find_movie_by_category(genre, collection):
    return collection.find({"genres": genre})


def get_list_from_cursor(cursor):
    objects = []
    for elem in cursor:
        objects.append(elem)
    return objects


def get_name_list_from_cursor(cursor):
    objects = []
    for elem in cursor:
        objects.append(elem["name"])
    return objects


def find_movie_reviews(movie_name, movie_collection, review_collection):
    movie_id = get_id_of_object(movie_name, movie_collection)
    return review_collection.find({"movie": movie_id})


def find_user_reviews(user_id, review_collection):
    return review_collection.find({"user": user_id})


def count_movie_reviews(movie_name, movie_collection, review_collection):
    movie_id = get_id_of_object(movie_name, movie_collection)
    return review_collection.find({"movie": movie_id}).count()


def count_user_reviews(user_name, user_collection, review_collection):
    user_id = get_id_of_object(user_name, user_collection)
    return review_collection.find({"user": user_id}).count()


def average_rating(movie_id, review_collection):
    a = review_collection.aggregate([
        {"$match": {"movie_id": movie_id}},
        {"$group": {"_id": "movie_id", "avg": {"$avg": "$rating"}}}
    ])
    for bla in a:
        return bla['avg']
