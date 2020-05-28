import pymongo
import names as n
import random as r
from faker import Faker


def gen_genres(genres_base):
    genres = []
    r.shuffle(genres_base)
    genres.append(genres_base.pop())
    while genres_base:
        i = r.randint(0, 3)
        if r.randint(0, 1) == 1:
            return genres
        genres.append(genres_base.pop())
    return genres_base


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

    def __init__(self, name):
        self.name = name
        self.genres = []
        self.reviews = []

    @classmethod
    def gen_movie(cls, name_bases):
        name = gen_movie_name(name_bases[0], name_bases[1], name_bases[2])
        return Movie(name)


class Review:

    def __init__(self, rating, txt):
        self.rating = rating
        self.txt = txt
        self.user = None
        self.movie = None

    @classmethod
    def gen_review(cls):
        faker = Faker()
        rating = r.randint(1, 5)
        txt = faker.text()
        return Review(rating, txt)


genres = ["Action", "Romance", "Horror", "Comedy", "Thriller", "Adventure", "Family", "Fantasy", "Thriller", "Sci-fi",
          "History", "Document", "Parody", "Teen", "Kid", "Superheroes", "War"]

name_set1 = ["Great", "Big", "Scary", "Black", "White", "Holy", "Thrilling", "Vast", "White", "Imprisoned"]

name_set2 = [" Adventure", " City", " Person", " Castle", " Dwarf", " Elf", " Country", " Forest", " Museum",
             " Library", "Turtle"]

name_set3 = [" of Endless Fun", "", " of the Dead", " with Morgan Freeman", " that never returns", ""]

for i in range(10):
    print(gen_movie_name(name_set1, name_set2, name_set3))
