# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app.models import authors


class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        #calling on the authors table and returning all columns

        connection = connectToMySQL('books')
        results = connection.query_db(query)
        #setting connection to the books schema in MySQL. Setting results to the query I just called

        books = []
        for result in results:
            books.append( cls(result) )
            #creating a list of each result from the query. Will be a list of dictionaries. returning results below

        return books
    
    @classmethod
    def get_book(cls, id):
        query = "SELECT * FROM books WHERE id = %(id)s"

        modified_data ={
            'id': id
        }
        connection = connectToMySQL('books')
        results = connection.query_db(query, modified_data)
        book = []
        for result in results: 
            book.append(cls(result))
        return book

    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        #inserting values into the others table 
        modified_data = {
            'title': data['title'],
            'num_of_pages': data['num_of_pages'],
        }

        connection = connectToMySQL('books')
        results = connection.query_db(query, modified_data)
        #connecting to the db and setting results to the query with the modified data inputted

        return results

    