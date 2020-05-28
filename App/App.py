import pymongo
import time
from easygui import *

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]
title = "Biblioteka Filmowa"


def login(name, password):
    user = users_col.find_one({"name": name})
    if not user:
        print("wrong username or password")
        return None
    if user["password"] != password:
        print("wrong username or password")
        return None
    return user["_id"]


def register(name, password):
    if users_col.find_one({"name": name}):
        return None
    return users_col.insert_one({"name": name, "password": password}).inserted_id


def add_movie(name, genres, director, year):
    if movies_col.find_one({"name": name}):
        return None
    return movies_col.insert_one({"name": name, "genres": genres,
                                  "director": director, "year": year}).inserted_id


def start_box():
    choices = ["Zaloguj", "Zarejestruj", "Wyjdź"]
    choice = buttonbox("Witaj w bibliotece filmowej", title, choices)
    if choice == "Zaloguj":
        name, password = login_box()
        user_id = login(name, password)
        if not user_id:
            wrong_login_pass_box()
        else:
            welcome_box(user_id, name)
    elif choice == "Zarejestruj":
        register_box()


def login_box():
    name = enterbox("Wprowadź nazwę użytkownika", title)
    password = passwordbox("Wprowadź hasło", title)
    return name, password


def wrong_login_pass_box():
    msgbox("Niepoprawne nazwa użytkownika lub hasło")
    start_box()


def register_box():
    name, password = multenterbox("Wprowadź dane", title, ["Nazwa", "Hasło"])
    user_id = register(name, password)
    if not user_id:
        name_taken_box()
    else:
        welcome_box(user_id, name)


def name_taken_box():
    msgbox("Ta nazwa jest już zajęta")
    start_box()


def welcome_box(user_id, username):
    msgbox("Witaj " + username + ", zalogowałeś/aś/oś się pomyślnie", title)
    menu_box(user_id)


def menu_box(user_id):
    choice = buttonbox("Co chcesz zrobić", title, ["Wyjdź", "Przeglądaj filmy",
                                                   "Przeglądnij swoje oceny", "Dodaj film"])
    if choice == "Przeglądaj filmy":
        movies_box(user_id)
    elif choice == "Przeglądnij swoje oceny":
        my_reviews_box(user_id)
    elif choice == "Dodaj film":
        add_movie_box(user_id)


def movies_box(user_id):
    print("movies_box")


def my_reviews_box(user_id):
    print("my_reviews_box")


def add_movie_box(user_id):
    name = enterbox("Nazwa filmu", title)
    add_movie_box2(user_id, name)


def add_movie_box2(user_id, name):
    director = enterbox("Nazwa reżysera", title)
    add_movie_box3(user_id, name, director)


def add_movie_box3(user_id, name, director):
    genres = multenterbox("Gatunki", title, ["1", "2", "3", "4", "5", "6", "7", "8"])
    while "" in genres:
        genres.remove("")
    add_movie_box4(user_id, name, director, genres)


def add_movie_box4(user_id, name, director, genres):
    year = int(enterbox("Rok", title))
    movie_id = add_movie(name, genres, director, year)
    if not movie_id:
        movie_exists_box(user_id)
    else:
        movie_added_box(user_id, name)


def movie_exists_box(user_id):
    msgbox("Film o podanej nazwie już istnieje", title)
    menu_box(user_id)


def movie_added_box(user_id, name):
    msgbox("Pomyślnie dodano film " + name, title)
    menu_box(user_id)


start_box()