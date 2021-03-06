import pymongo
from easygui import *
from bson.objectid import ObjectId
from Functionalities import Functions as f

print("Connecting to client...")
client = pymongo.MongoClient("mongodb://localhost:27017")
print("Connected")
print("Accessing data...")
db = client["movies_library"]
movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]
print("Data accessed")
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


def insert_movie(name, genres, director, year):
    if movies_col.find_one({"name": name}):
        return None
    return movies_col.insert_one({"name": name, "genres": genres,
                                  "director": director, "year": year}).inserted_id


def insert_review(rating, text, user_id, movie_id):
    if reviews_col.find_one({"user_id": user_id, "movie_id": movie_id}):
        return None
    return reviews_col.insert_one({"rating": rating, "text": text,
                                   "user_id": ObjectId(user_id), "movie_id": ObjectId(movie_id)}).inserted_id


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
    y = ynbox("Chcesz filtrować wyniki?", title)
    if y:
        filter_box(user_id)
    else:
        movies = f.get_name_list_from_cursor(f.show_all_objects(movies_col))
        choice = choicebox(msg="Wybierz film", title=title, choices=movies)
        if choice is not None:
            display_movie_box(choice, user_id)
        else:
            menu_box(user_id)


def filter_box(user_id):
    choice = choicebox("Wybierz kategorię", title, choices=["gatunek", "reżyser", "rok produkcji"])
    made_a_choice = True
    movies = None
    if choice is None:
        check_continue_browsing_box(user_id)
    else:
        if choice == "gatunek":
            genre = choicebox("Wybierz gatunki", title, genres_set)
            if genre is not None:
                movies = f.get_name_list_from_cursor(f.find_movie_by_category(genre, movies_col))
            else:
                made_a_choice = False
        elif choice == "reżyser":
            director = enterbox(msg="Podaj imię i nazwisko reżysera", title=title)
            if director is not None:
                movies = f.get_name_list_from_cursor(f.find_movie_by_director(director, movies_col))
            else:
                made_a_choice = False
        elif choice == "rok produkcji":
            if ynbox("Czy chcesz wybra rok produkcji jako przedział?", title):
                year0 = integerbox("Podaj początek przedziału", title, upperbound=10000)
                year = integerbox("Podaj koniec przedziału", title, upperbound=10000)
                if year0 is not None and year is not None:
                    movies = f.get_name_list_from_cursor(f.find_movie_by_year_margin(year0, year, movies_col))
                else:
                    made_a_choice = False
            else:
                year = integerbox("Podaj rok", title, upperbound=10000)
                if year is not None:
                    movies = f.get_name_list_from_cursor(f.find_movie_by_year(year, movies_col))
                else:
                    made_a_choice = False
        else:
            made_a_choice = False
    if made_a_choice:
        if len(movies) == 1:
            display_movie_box(movies[0], user_id)
        elif len(movies) > 0:
            choice = choicebox(msg="Wybierz film", title=title, choices=movies)
            display_movie_box(choice, user_id)
        else:
            msgbox("Nie znaleziono filmów spełniających wybrane kryteria", title)
            check_continue_browsing_box(user_id)
    else:
        check_continue_browsing_box(user_id)


def display_movie_box(movie_name, user_id):
    movie_cursor = f.find_object_by_name(movie_name, movies_col)
    movie = movie_cursor[0]
    genres = ""
    for i in movie["genres"]:
        genres += i
        genres += ", "
    rat = f.average_rating(movie["_id"], reviews_col)
    if rat is None:
        rat = "Brak ocen"
    else:
        rat = "Średnia ocen: " + str(rat)
    choice = buttonbox(movie["name"] + "\n" + "Gatunki: " + genres + "\n" + "Reżyser: " + movie["director"] + "\n"
                       + rat + "\n" + "Ilość recenzji: "
                       + str(f.count_movie_reviews(movie["name"], movies_col, reviews_col)),
                       title, ["Oceń", "Wyjdź", "Oceny"])
    if choice == "Oceń":
        add_review_box(movie["_id"], user_id)
    elif choice == "Oceny":
        reviews_of_movie_box(movie_name, user_id)
    else:
        check_continue_browsing_box(user_id)


def add_review_box(movie_id, user_id):
    rating = integerbox("Podaj jak oceniasz film w skali 1-5", title, lowerbound=1, upperbound=5)
    if rating is not None:
        add_review_box2(movie_id, user_id, rating)
    else:
        menu_box(user_id)


def add_review_box2(movie_id, user_id, rating):
    text = enterbox("Co sądzisz o filmie?", title)
    if text is not None:
        review = insert_review(rating, text, user_id, movie_id)
        if not review:
            review_exists(user_id)
        else:
            review_added(user_id, movie_id)
    else:
        menu_box(user_id)


def review_exists(user_id):
    msgbox("Oceniłeś już dany film", title)
    menu_box(user_id)


def review_added(user_id, movie_id):
    msgbox("Pomyślnie dodano recenzję filmu " + str(f.get_name_of_object(movie_id, movies_col)), title)
    menu_box(user_id)


def reviews_of_movie_box(movie_name, user_id):
    reviews = f.find_movie_reviews(movie_name, movies_col, reviews_col)
    if reviews.count() == 0:
        msgbox("Ten film nie ma ocen", title)
        menu_box(user_id)
    else:
        review_names = []
        review_objects = []
        for review in reviews:
            review_objects.append(review)
            review_names.append(f.get_name_of_object(review['user_id'], users_col))
        choice = choicebox("Recenzje filmu:", title, review_names)
        review_box(user_id, review_objects[review_names.index(choice)], movie_name)


def check_continue_browsing_box(user_id):
    if ccbox("Czy chcesz wrócić do ekranu przeglądania filmów?", title):
        movies_box(user_id)
    else:
        menu_box(user_id)


def my_reviews_box(user_id):
    reviews = f.find_user_reviews(user_id, reviews_col)
    if reviews.count() == 0:
        msgbox("Nie oceniłeś/aś żadnych filmów", title)
        menu_box(user_id)
    else:
        reviews_names_obj = {}
        for review in reviews:
            movie_id = review["movie_id"]
            reviews_names_obj[f.get_name_of_object(movie_id, movies_col)] = review
        reviews_names = []
        for name in reviews_names_obj.keys():
            reviews_names.append(name)
        choice = choicebox("Twoje oceny", title, reviews_names)
        chosen_review = reviews_names_obj[choice]
        review_box(user_id, chosen_review, choice)


def review_box(user_id, review, movie_name):
    author = f.get_name_of_object(review["user_id"], users_col)
    msgbox("Autor recenzji: " + author + "\n" + "Tytuł: " + movie_name + "\n" + "Ocena: " + str(review["rating"]) + "\n"
           + "Recenzja: " + "\n" + str(review["text"]), title)
    menu_box(user_id)


def add_movie_box(user_id):
    name = enterbox("Nazwa filmu", title)
    if name == "":
        msgbox("Nie podano nazwy", title)
        menu_box(user_id)
        return
    add_movie_box2(user_id, name)


def add_movie_box2(user_id, name):
    director = enterbox("Nazwa reżysera", title)
    if director == "":
        msgbox("Nie podano nazwy reżysera", title)
        menu_box(user_id)
        return
    add_movie_box3(user_id, name, director)


def add_movie_box3(user_id, name, director):
    genres = multchoicebox("Gatunki", title, genres_set)
    while "" in genres:
        genres.remove("")
    add_movie_box4(user_id, name, director, genres)


def add_movie_box4(user_id, name, director, genres):
    year = enterbox("Rok", title)
    if not year.isnumeric():
        msgbox("Rok produkcji musi być liczbą", title)
        menu_box(user_id)
        return
    year = int(year)
    if year < 0 or year > 10000:
        msgbox("To nie jest poprawna data")
        menu_box(user_id)
        return
    movie_id = insert_movie(name, genres, director, year)
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
