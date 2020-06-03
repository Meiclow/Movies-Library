import string

import pymongo
import names as n
import random as r
from faker import Faker
from Functionalities import Functions as f


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

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @classmethod
    def gen_user(cls):
        name = n.get_full_name()
        size = r.randint(8, 20)
        password = ''.join(r.choice(string.ascii_letters + string.digits) for _ in range(size))
        return User(name, password)


class Movie:

    def __init__(self, name, genres, director, year):
        self.name = name
        self.genres = genres
        self.director = director
        self.year = year

    @classmethod
    def gen_movie(cls, name_bases, genres_base):
        name = gen_movie_name(name_bases[0], name_bases[1], name_bases[2])
        genres = gen_genres(genres_base)
        director = n.get_full_name()
        year = r.randint(1920, 2020)
        return Movie(name, genres, director, year)


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


genres_set = ["Action", "Romance", "Horror", "Comedy", "Thriller", "Adventure", "Family", "Fantasy", "Thriller",
              "Sci-fi", "History", "Document", "Parody", "Teen", "Kid", "Superheroes", "War", "Drama", "Educational",
              "Short", "Animated"]

name_set1 = ["Great", "Big", "Scary", "Black", "White", "Holy", "Thrilling", "Vast", "White", "Imprisoned", "Endless",
             "The Best", "Awful", "Tiny", "Little", "Demonic", "Sturdy"]

name_set2 = [" Adventure", " City", " Person", " Castle", " Dwarf", " Elf", " Country", " Forest", " Museum",
             " Library", "Turtle", " Samurai", " Detective", " Lamb", " Sorcerer", " Demon", " King"]

name_set3 = [" of Endless Fun", "", " of the Dead", " with Morgan Freeman", " that never returns", "", " on the Couch",
             " - that's what she said", " or not", "", ", Real Story", "", " and the Others"]

name_sets = [name_set1, name_set2, name_set3]

client = pymongo.MongoClient("mongodb://localhost:27017")
# client.drop_database("movies_library")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]


def insert_user(user: User):
    if users_col.find_one({"name": user.name}):
        return None
    return users_col.insert_one({"name": user.name, "password": user.password}).inserted_id


def insert_movie(movie: Movie):
    if movies_col.find_one({"name": movie.name}):
        return None
    return movies_col.insert_one({"name": movie.name, "genres": movie.genres,
                                  "director": movie.director, "year": movie.year}).inserted_id


def insert_review(review: Review):
    if reviews_col.find_one({"user_id": review.user, "movie_id": review.movie}):
        return None
    review_id = reviews_col.insert_one({"rating": review.rating, "text": review.txt,
                                        "user_id": review.user, "movie_id": review.movie}).inserted_id
    return review_id


r.seed()
u_ids = []
m_ids = []

for i in range(100):
    u_ids.append(insert_movie(Movie.gen_movie(name_sets, genres_set)))
    m_ids.append(insert_user(User.gen_user()))
for i in range(100):
    u_id = r.choice(u_ids)
    m_id = r.choice(m_ids)
    insert_review(Review.gen_review(u_id, m_id))
