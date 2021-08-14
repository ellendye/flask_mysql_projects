# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save_information(cls, data):
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"

        modified_data = {
            'email': data['email']
        }

        connection = connectToMySQL('email_schema')
        results = connection.query_db(query, modified_data)
        flash("SUCCESSFUL EMAIL! Good job")
        return results

    @classmethod
    def delete_email(cls, id):
        query = "DELETE FROM emails WHERE id = %(id)s;"

        modified_data = {
            'id': id
        }

        connection = connectToMySQL('email_schema')
        results = connection.query_db(query, modified_data)

        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"

        connection = connectToMySQL('email_schema')
        results = connection.query_db(query)

        emails = []
        for result in results:
            emails.append( cls(result) )

        return emails

    @staticmethod
    def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
            return is_valid

        query = "SELECT email FROM emails WHERE email = %(email)s;"
        modified_data = {
            'email': user['email']
        }
        connection = connectToMySQL('email_schema')
        results = connection.query_db(query, modified_data)
        print(results)
        if len(results) > 0:
            is_valid = False
            flash("This email is not unique")


        return is_valid