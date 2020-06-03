import pymongo
import time
from easygui import *

from Functionalities import Functions as f
from Generator import Generator as g

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]
title = "Biblioteka Filmowa"

genres_set = ["Action", "Romance", "Horror", "Comedy", "Thriller", "Adventure", "Family", "Fantasy", "Thriller",
              "Sci-fi", "History", "Document", "Parody", "Teen", "Kid", "Superheroes", "War", "Drama", "Educational",
              "Short", "Animated"]


def login(name, password):
    user = users_col.find_one({"name": name})
    if not user:
        return None
    if user["password"] != password:
        return None
    return user["_id"]


def register(name, password):
    if users_col.find_one({"name": name}):
        return None
    return users_col.insert_one({"name": name, "password": password}).inserted_id


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
    if ynbox("Chcesz filtrować wyniki?", title):
        filter_box(user_id)
    else:
        movies = f.gat_name_list_from_cursor(f.show_all_objects(movies_col))
        choice = choicebox(msg="Pick a movie", choices=movies)
        display_movie_box(choice, user_id)


def filter_box(user_id):
    choice = choicebox("Wybierz kategorię", title, choices=["gatunek", "reżyser", "rok produkcji"])
    made_a_choice = True
    movies = None
    if choice is None:
        check_continue_browsing_box(user_id)
    else:
        if choice == "gatunek":
            genre = choicebox("Wybierz gatunki", title, g.genres_set)
            if genre is not None:
                movies = f.gat_name_list_from_cursor(f.find_movie_by_category(genre, movies_col))
            else:
                made_a_choice = False
        elif choice == "reżyser":
            director = enterbox(msg="Podaj imię i nazwisko reżysera", title=title)
            if director is not None:
                movies = f.gat_name_list_from_cursor(f.find_movie_by_director(director, movies_col))
            else:
                made_a_choice = False
        elif choice == "rok produkcji":
            if ynbox("Czy chcesz wybra rok produkcji jako przedział?", title):
                year0 = integerbox("Podaj początek przedziału", title, lowerbound=1919, upperbound=2020)
                year = integerbox("Podaj koniec przedziału", title, lowerbound=1919, upperbound=2020)
                if year0 is not None and year is not None:
                    movies = f.gat_name_list_from_cursor(f.find_movie_by_year_margin(year0, year, movies_col))
                else:
                    made_a_choice = False
            else:
                year = integerbox("Podaj rok", title, lowerbound=1919, upperbound=2020)
                if year is not None:
                    movies = f.gat_name_list_from_cursor(f.find_movie_by_year(year, movies_col))
                else:
                    made_a_choice = False
        else:
            made_a_choice = False
    if made_a_choice:
        if len(movies) == 1:
            display_movie_box(movies[0], user_id)
        elif len(movies) > 0:
            choice = choicebox(msg="Pick a movie", choices=movies)
            display_movie_box(choice, user_id)
        else:
            msgbox("Nie znaleziono filmów spełniających wybrane kryteria", title)
            check_continue_browsing_box(user_id)
    else:
        check_continue_browsing_box(user_id)

        """new_cursor = f.showAllObjects(movies_col)
        if "gatunek" in choices:
            genre_list = multchoicebox("Wybierz gatunki", title, g.genres_set)
            if genre_list is not None:
                for genre in genre_list:
                    new_cursor = f.findMovieByCategory(genre, new_movie_col)
                    for object in new_cursor:
        if "reżyser" in choices:
            director = enterbox(msg="Podaj imię i nazwisko reżysera", title=title)
            if director is not None:
                new_movie_col = f.findMovieByDirector(director, new_movie_col)
        if "rok produkcji" in choices:
            if ynbox("Czy chcesz wybra rok produkcji jako przedział?", title):
                year0 = integerbox("Podaj początek przedziału", title)
                year = integerbox("Podaj koniec przedziału", title)
                if year0 is not None and year is not None:
                    new_movie_col = f.findovieByYearMargin(year0, year, new_movie_col)
            else:
                year = integerbox("Podaj rok", title)
                new_movie_col = f.findovieByYear(year, new_movie_col)
        movies = f.showAllObjects(new_movie_col)
        choices = []
        for movie in movies:
            choices.append(movie["name"])
        choice = choicebox(msg="Pick a movie", choices=choices)
        display_movie_box(choice, user_id)"""


def display_movie_box(movie_name, user_id):
    movie_cursor = f.find_object_by_name(movie_name, movies_col)

    for movie in movie_cursor:
        genres = ""
        for i in movie["genres"]:
            genres += i
            genres += ", "
        msgbox(movie["name"] + "\n" + "gatunki: " + genres + "\n" + "Reżyser: " + movie["director"] + "\n"
               + "Rok produkcji: " + str(movie["year"]) + "\n" + "Średnia ocena: "
               + str(f.average_rating(movie["_id"], movies_col))
               + "\n" + "Ilość recenzji: " + str(f.count_movie_reviews(movie["name"], movies_col, reviews_col)))
        break

    check_continue_browsing_box(user_id)


def check_continue_browsing_box(user_id):
    if ccbox("Do you want to continue browsing?"):
        movies_box(user_id)
    else:
        menu_box(user_id)


def my_reviews_box(user_id):
    print("my_reviews_box")


def add_movie_box(user_id):
    name = enterbox("Nazwa filmu", title)
    add_movie_box2(user_id, name)


def add_movie_box2(user_id, name):
    director = enterbox("Nazwa reżysera", title)
    add_movie_box3(user_id, name, director)


def add_movie_box3(user_id, name, director):
    genres = multchoicebox("Gatunki", title, genres_set)
    while "" in genres:
        genres.remove("")
    add_movie_box4(user_id, name, director, genres)


def add_movie_box4(user_id, name, director, genres):
    year = int(enterbox("Rok", title))
    movie_id = g.insert_movie(g.Movie(name, genres, director, year))
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
