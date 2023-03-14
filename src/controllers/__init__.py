from controllers.authentication_controller import auth
from controllers.home_controller import home
from controllers.book_controller import books
from controllers.author_controller import authors
from controllers.publisher_controller import publishers
from controllers.production_controller import production
from controllers.director_controller import directors
from controllers.movie_controller import movies
from controllers.read_controller import read
from controllers.watched_controller import watched


registerable_controllers = [
    home,
    auth,
    books,
    authors,
    publishers,
    production,
    directors,
    movies,
    read,
    watched
]