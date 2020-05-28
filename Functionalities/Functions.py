import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]

def findObjectByName(name, collection):
    return collection.find({"name": name})

def findovieByYear(year, collection):
    return collection.find({"year": year})

def findovieByYearMargin(yearFrom, yearTo, collection):
    return collection.find({"$and": [{"year": {"$gte": yearFrom}},{"year": {"$lte": yearTo}} ]})

def findMovieByRating(rating, collection):
    return collection.find({"rating": rating})

def findovieByRatingMargin(ratingFrom, ratingTo, collection):
    return collection.find({"$and": [{"rating": {"$gte": ratingFrom}}, {"rating": {"$lte": ratingTo}}]})

def findMovieByDirector(director, collection):
    return collection.find({"director": director})

def findMovieByCategory(category, collection):
    return collection.find({"category"})