# Movies-Library
### Mini-projekt z przedmiotu Bazy Danych


## 1. Wstęp

W ramach przedmiotu Bazy Danych zdecydowaliśmy się na stworzenie aplikacji bazodanowej przechowującej kolekcję filmów oraz ich recenzji. Do tego celu wykorzystaliśmy technologię Mongo. Sama aplikacja została napisana w języku Python pomocy biblioteki pymongo. Jako biblioteka pomocnicza posłużyło nam bson, a głównie moduł objectid, dzięki któremu mogliśmy definiować relacje między obiektami w bazie.

## 2. Struktura bazy

Baza składa się z trzech kolekcji dokumentów. Poniżej je wymieniliśmy, opisaliśmy, oraz wypisaliśmy ich potencjalne pola:
  1. Users - kolekcja użytkowników bazy:
     - _id - identyfikator
     - name - nazwa użytkownika
     - password - hasło przy pomocy którego użytkownik się loguje do aplikacji
```
{
    "_id" : ObjectId("5ed7f43141958df24196be9f"),
    "name" : "Kurt Konrad",
    "password" : "z981e7sfssXOebmUaJ"
}
```
2. Movies - kolekcja filmów w bazie:
     - _id - identyfikator
     - name - tytuł filmu
     - genres - zbiór gatunków pod które można podpiąć dany film
     - director - nazwa reżysera
     - year - rok produkcji
```
{
    "_id" : ObjectId("5ed7f43041958df24196be9e"),
    "name" : "Imprisoned Samurai of the Dead",
    "genres" : [ 
        "Short", 
        "War"
    ],
    "director" : "Valerie Woodard",
    "year" : 1961
}
```
3. Reviews - kolekcja recenzji filmów:
     - _id - identyfikator
     - rating - ocena w skali 1 - 5
     - text - treść recenzji
     - user_id - identyfikator oceniającego użytkownika
     - movie_id - identyfikator ocenianego filmu
```
{
    "_id" : ObjectId("5ed7f48041958df24196c0b5"),
    "rating" : 2,
    "text" : "Item himself future free event. Throughout official wide clearly.",
    "user_id" : ObjectId("5ed7f43241958df24196bebb"),
    "movie_id" : ObjectId("5ed7f43641958df24196bf63")
}
```
Jak widać w trakcie projektowania struktury bazy staraliśmy się zminimalizować redundancję danych, w wyniku czego udało nam się ją całkowicie zniwelować.

## 3. Generator
Następnie przystąpiliśmy do napisania generatora, dzięki któremu możliwe byłoby testowanie działa bazy dla dużych ilości danych. Kod generatora znajduje się w pliku Generator.py w folderze Generator. Przy jego realizacji skorzystaliśmy z następujących bibliotek:
- string - w celu generowania haseł
- names - w celu generowania nazw użytkowników i reżyserów
- faker - w celu generowania treści recenzji
- random - w celu generowania ocen filmów

Domyślnie generator tworzy około 100 użytkowników, 100 filmów i 340 recenzji.

## 4. Back-end

W dalszej kolejności przystąpiliśmy do realizacji fukcji, które umożliwiłyby nam wyszukiwanie, modyfikowanie i agregowanie obiektów bazy. Wszystkie stworzone w ten sposób funkcję znajdują się w pliku Functions.py w folderze Functionalities.

## 5. Front-end

Następnie stworzyliśmy warstwę front-end. Nie skupialiśmy się na wizualnej oprawie aplikacji, stąd zdecydowaliśmy się na użycie prostej w użyciu biblioteki easygui. Umożliwia ona tworzenie okienkowego gui w stylu kaskadowym (po każdym oknie wyświetlane jest następne w zależności od inputu w poprzednich).

## 6. Realizowana funkcjonalność

W aktualnym stanie aplikacji użytkownik może:
- rejestrować się w aplikacji
- logować się do aplikacji
- przeglądać wszystkie filmy w bazie
- przeglądać filmy przefiltrowane przez gatunki, reżysera lub rok produkcji
- dodawać recenzję do wybranych filmów (jest w tym ograniczony, poprzez maksymalnie jedną recenzję na film)
- przeglądać recenzje danego filmu
- przeglądać własne recenzje filmów
- dodawać filmy do bazy







