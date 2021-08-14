from flask_app import app

from flask import render_template, redirect, session, request

from flask_app.models.authors import Author#name of model file# import #name of class#
from flask_app.models.books import Book

@app.route("/")
def index():
    # redirecting to the /authors location per the wireframe
    return redirect("/author")

@app.route("/author")
def show_authors():
    #rendering the authors.html template and showing all authors
    authors = Author.get_all()
    return render_template("authors.html", authors=authors)

@app.route("/author/<int:id>")
def show_author(id):
    #rendering the authors.html template and showing all authors
    author = Author.get_author(id)
    books = Author.testing(id)
    return render_template("show_author.html", author = author, books =books)


@app.route("/author/create", methods=['POST'])
def create_author():
    #rendering the authors.html template and showing all authors
    Author.create_author(request.form)
    return redirect("/")

@app.route("/author/<int:id>/addfavorite", methods=['POST'])
def add_favorite_author(id):
    #sending the request.form and id to the add author favorite template. redirecting back to the specific authors page
    Author.add_favorite(request.form, id)
    return redirect(f"/author/{id}")

@app.route("/book")
def show_books():
    #rendering the authors.html template and showing all authors
    books = Book.get_all()
    return render_template("books.html", books = books)

@app.route("/book/create", methods=['POST'])
def create_book():
    #rendering the authors.html template and showing all authors
    print(request.form)
    Book.create_book(request.form)
    return redirect("/book")

@app.route("/book/<int:id>")
def show_book(id):
    #rendering the authors.html template and showing all authors
    books = Author.get_book(id)
    authors = Author.get_author_not_liked(id)
    
    return render_template(f"show_book.html", books = books, authors = authors)


@app.route("/book/<int:id>/addfavorite", methods=['POST'])
def add_favorite_book(id):
    #sending the request.form and id to the add author favorite template. redirecting back to the specific authors page
    Author.add_favorite(request.form, id)
    return redirect(f"/book/{id}")