from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import books

class Author: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.books = None
        self.favorites = None
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        #calling on the authors table and returning all columns

        connection = connectToMySQL('books')
        results = connection.query_db(query)
        #setting connection to the books schema in MySQL. Setting results to the query I just called

        authors = []
        for result in results:
            authors.append( cls(result) )
            #creating a list of each result from the query. Will be a list of dictionaries. returning results below

        return authors


    @classmethod
    def create_author(cls, data):
        query = "INSERT INTO authors (first_name, last_name, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, NOW(), NOW());"
        #inserting calues into the others table 
        modified_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
        }

        connection = connectToMySQL('books')
        results = connection.query_db(query, modified_data)
        #connecting to the db and setting results to the query with the modified data inputted

        return results
    
    @classmethod
    def get_author(cls, author_id):
        query = "SELECT authors.id as id, authors.created_at as created_at, authors.updated_at as updated_at, book_id, books.created_at as books_created_at, books.updated_at as books_updated_at, first_name, last_name, title, num_of_pages FROM authors lEFT JOIN favorites ON author_id = authors.id LEFT JOIN books ON book_id = books.id WHERE authors.id = %(id)s;"
        #calling on the authors table and returning all columns where the id is equal to the id from data
        data = {
        'id': author_id
        
        }
        #setting id to the id passed in from controller
        connection = connectToMySQL('books')
        results = connection.query_db(query, data)
        #setting results equal to the query called with the data passed in that i just set
        #creating an array of this authors favorite books
        favorite_books = []
        for result in results:
            books_info = {
                'id': result['book_id'],
                'title': result['title'],
                'num_of_pages': result['num_of_pages'],
                'created_at': result['books_created_at'],
                'updated_at': result['books_updated_at']
            }
            faves = cls(result)
            faves.books = books.Book(books_info)
            favorite_books.append(faves)
        return favorite_books


    @classmethod
    def add_favorite(cls, data, id):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s)"
        #calling on the favorites table and entering in the author id and the book id
        modified_data = {
            'book_id': data['book_id'],
            'author_id': id
        }

        connection = connectToMySQL('books')
        results = connection.query_db(query, modified_data)
        #setting results equal to the query called with the modified data that i just set

        return results

    @classmethod
    def get_book(cls, book_id):
        query = "SELECT authors.id as id, authors.created_at as created_at, authors.updated_at as updated_at, book_id, books.created_at as books_created_at, books.updated_at as books_updated_at, first_name, last_name, title, num_of_pages FROM books lEFT JOIN favorites ON book_id = books.id LEFT JOIN authors ON author_id = authors.id WHERE books.id = %(id)s;"
        #calling on the authors table and returning all columns where the id is equal to the id from data
        data = {
        'id': book_id
        
        }
        #setting id to the id passed in from controller
        connection = connectToMySQL('books')
        results = connection.query_db(query, data)
        #setting results equal to the query called with the data passed in that i just set
        #creating an array of this authors favorite books
        favorite_authors = []
        for result in results:
            books_info = {
                'id': result['book_id'],
                'title': result['title'],
                'num_of_pages': result['num_of_pages'],
                'created_at': result['books_created_at'],
                'updated_at': result['books_updated_at']
            }
            faves = cls(result)
            faves.books = books.Book(books_info)
            favorite_authors.append(faves)
            print(result)
        return favorite_authors

    @classmethod
    def get_author_not_liked(cls, book_id):
        authors_who_liked = cls.get_book(book_id)
        authors = cls.get_all()
        
        new_list = []
        for author in authors_who_liked:
            new_list.append(author.id)

        authors_not_liked = []
        for author in authors:
            if author.id not in new_list:
                authors_not_liked.append(author)
            
        return authors_not_liked 
    
    @classmethod
    def get_books_not_liked(cls, author_id):
        books_liked = cls.get_author(author_id)
        all_books = books.Book.get_all()

        new_list = []
        for book in books_liked:
            new_list.append(book.books.id)

        books_not_liked = []
        for book in all_books:
            if book.id not in new_list:
                books_not_liked.append(book)

        
        return books_not_liked


    @classmethod
    def testing(cls, author_id):
        query = "SELECT authors.id as id, authors.created_at as created_at, authors.updated_at as updated_at, book_id, books.created_at as books_created_at, books.updated_at as books_updated_at, first_name, last_name, title, num_of_pages FROM books LEFT JOIN favorites ON book_id = books.id LEFT JOIN authors ON author_id = authors.id WHERE title NOT IN (SELECT title FROM books LEFT JOIN favorites ON book_id = books.id LEFT JOIN authors ON author_id = authors.id WHERE authors.id = %(id)s) GROUP BY title;"

        modified_data = {
            'id': author_id
        }
        connection = connectToMySQL('books')
        results = connection.query_db(query, modified_data)

        books_not_liked = []
        for result in results:
            books_info = {
                'id': result['book_id'],
                'title': result['title'],
                'num_of_pages': result['num_of_pages'],
                'created_at': result['books_created_at'],
                'updated_at': result['books_updated_at']
            }
            not_liked = cls(result)
            not_liked.books = books.Book(books_info)
            books_not_liked.append(not_liked)

        return books_not_liked