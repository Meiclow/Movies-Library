import pymongo
from bson import ObjectId

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


def get_name_of_object(id, collection):
    a = collection.find({"_id": id}, {"name": 1, "_id": 0})
    for bla in a:
        return bla['name']


def find_object_by_name(name, collection):
    return collection.find({"name": name})


def find_movie_by_year(year, collection):
    return collection.find({"year": year})


def find_movie_by_year_margin(yearFrom, yearTo, collection):
    return collection.find({"$and": [{"year": {"$gte": yearFrom}}, {"year": {"$lte": yearTo}}]})


def find_movie_by_rating(rating, collection):
    return collection.find({"rating": rating})


def find_movie_by_rating_margin(ratingFrom, ratingTo, collection):
    return collection.find({"$and": [{"rating": {"$gte": ratingFrom}}, {"rating": {"$lte": ratingTo}}]})


def find_movie_by_director(director, collection):
    return collection.find({"director": director})


def find_movie_by_category(genre, collection):
    return collection.find({"genres": genre})


def get_list_from_cursor(cursor):
    objects = []
    for elem in cursor:
        objects.append(elem)
    return objects


def gat_name_list_from_cursor(cursor):
    objects = []
    for elem in cursor:
        objects.append(elem["name"])
    return objects


def find_movie_reviews(movieName, Moviecollection, ReviewCollection):
    movie_id = get_id_of_object(movieName, Moviecollection)
    return ReviewCollection.find({"movie": movie_id})


def find_user_reviews(userName, userCollection, ReviewCollection):
    userID = get_id_of_object(userName, userCollection)
    return ReviewCollection.find({"user": userID})


def count_movie_reviews(movieName, Moviecollection, ReviewCollection):
    movieId = get_id_of_object(movieName, Moviecollection)
    return ReviewCollection.find({"movie": movieId}).count()


def count_user_reviews(userName, userCollection, ReviewCollection):
    userID = get_id_of_object(userName, userCollection)
    return ReviewCollection.find({"user": userID}).count()


def average_rating(movieID, reviewCollection):
    a = reviewCollection.aggregate([
        {"$match": {"movie_id": movieID}},
        {"$group": {"_id": "movie_id", "avg": {"$avg": "$rating"}}}
    ])
    for bla in a:
        return bla['avg']
