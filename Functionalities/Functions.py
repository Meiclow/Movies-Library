import pymongo


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
    movieId = Moviecollection.find({"name": name})
    return collection.find({})