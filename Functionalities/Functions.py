import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]

def getIDOfObject(name, collection):
    a = collection.find({"name": name}, {"_id": 1})
    print(a)
    for bla in a:
        print(bla)
        print(bla[0])
        return bla['_id']

def getNameOfObject(id, collection):
    a = collection.find({"_id": id}, {"name": 1, "_id": 0})
    print(a)
    for bla in a:
        print(bla)
        print(bla['name'])
        return bla['name']

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

def findMovieByCategory(genre, collection):
    return collection.find({"genres": genre})

def findMovieReviews(movieName, Moviecollection, ReviewCollection):
    movieId = getIDOfObject(movieName, Moviecollection)
    return ReviewCollection.find({"movie": movieId})

def findUserReviews(userName, userCollection, ReviewCollection):
    userID = getIDOfObject(userName, userCollection)
    return ReviewCollection.find({"user": userID})

def countMovieReviews(movieName, Moviecollection, ReviewCollection):
    movieId = getIDOfObject(movieName, Moviecollection)
    return ReviewCollection.find({"movie": movieId}).count()

def countUserReviews(userName, userCollection, ReviewCollection):
    userID = getIDOfObject(userName, userCollection)
    return ReviewCollection.find({"user": userID}).count()

def aggregateReviewsByMovie(Moviecollection, ReviewCollection):
    return ReviewCollection.aggregate([
        {"$group": {"_id": getNameOfObject("id", Moviecollection), "count": {"$sum": 1}}},
        {"$sort": {"count": 1}}
    ])

print(aggregateReviewsByMovie(movies_col, reviews_col))
