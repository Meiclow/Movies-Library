import pymongo
import names as n
import random as r
from faker import Faker


def gen_genres(genres_base):
    copy = genres_base.copy()
    genres = []
    r.shuffle(copy)
    genres.append(copy.pop())
    while copy:
        i = r.randint(0, 3)
        if r.randint(0, 1) == 1:
            return genres
        genres.append(copy.pop())
    return genres


def gen_movie_name(first_base, second_base, third_base):
    return r.choice(first_base) + r.choice(second_base) + r.choice(third_base)


class User:

    def __init__(self, name):
        self.name = name
        self.reviews = []

    @classmethod
    def gen_user(cls):
        name = n.get_full_name()
        return User(name)


class Movie:

    def __init__(self, name, genres):
        self.name = name
        self.genres = genres
        self.reviews = []

    @classmethod
    def gen_movie(cls, name_bases, genres_base):
        name = gen_movie_name(name_bases[0], name_bases[1], name_bases[2])
        genres = gen_genres(genres_base)
        return Movie(name, genres)


class Review:

    def __init__(self, rating, txt, user_id, movie_id):
        self.rating = rating
        self.txt = txt
        self.user = user_id
        self.movie = movie_id

    @classmethod
    def gen_review(cls, user_id, movie_id):
        faker = Faker()
        rating = r.randint(1, 5)
        txt = faker.text()
        return Review(rating, txt, user_id, movie_id)


genres_set = ["Action", "Romance", "Horror", "Comedy", "Thriller", "Adventure", "Family", "Fantasy", "Thriller", "Sci-fi",
          "History", "Document", "Parody", "Teen", "Kid", "Superheroes", "War"]

name_set1 = ["Great", "Big", "Scary", "Black", "White", "Holy", "Thrilling", "Vast", "White", "Imprisoned"]

name_set2 = [" Adventure", " City", " Person", " Castle", " Dwarf", " Elf", " Country", " Forest", " Museum",
             " Library", "Turtle"]

name_set3 = [" of Endless Fun", "", " of the Dead", " with Morgan Freeman", " that never returns", ""]

name_sets = [name_set1, name_set2, name_set3]

client = pymongo.MongoClient("mongodb://localhost:27017")
client.drop_database("movies_library")
client.drop_database("MichalDronka6")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]


def insert_user(user: User):
    if users_col.find_one({"name": user.name}):
        print("This name is already taken")
        return None
    return users_col.insert_one({"name": user.name})


def insert_movie(movie: Movie):
    if movies_col.find_one({"name": movie.name}):
        print("Movie with this name already exists")
        return None
    return movies_col.insert_one({"name": movie.name, "genres": movie.genres})


def insert_review(review: Review):
    """
    if reviews_col.find_one({"user_id": review.user, "movie_id": review.movie}):
        print("This user already rated this movie")
        return None
    """
    review_id = reviews_col.insert_one({"rating": review.rating, "text": review.txt,
                                        "user_id": review.user, "movie_id": review.movie}).inserted_id
    users_col.update({"_id": review.user}, {"$push": {"reviews": review_id}})
    movies_col.update({"_id": review.movie}, {"$push": {"reviews": review_id}})
    return review_id


u_ids = []
m_ids = []
for i in range(100):
    u_ids.append(insert_movie(Movie.gen_movie(name_sets, genres_set)))
    m_ids.append(insert_user(User.gen_user()))
for i in range(100):
    u_id = r.choice(u_ids)
    m_id = r.choice(m_ids)
    insert_review(Review.gen_review(u_id, m_id))
