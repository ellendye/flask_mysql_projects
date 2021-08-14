from flask import app, flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
first_name = re.compile(r'^[a-zA-Z]{2,45}$')
last_name = re.compile(r'^[a-zA-Z]{2,45}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #method to add user to database. saves user information. password is already hashed.
    @classmethod
    def save_information(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        
        connection = connectToMySQL('registration_schema')
        results = connection.query_db(query, data)

        flash("Successful registration! Welcome to our website!")
        
        return results

    #get user information class. check to see if i'm saving wrong. Don't think i should be doing results[0]
    @classmethod
    def get_user(cls, data):
        query = "SELECT first_name, id FROM users WHERE email = %(email)s"

        modified_data= {
            'email': data['email']
        }

        connection = connectToMySQL('registration_schema')
        results = connection.query_db(query, modified_data)

        user = results[0]
        return user
    
    #validate user loging function. check to see if i'm saving wrong. don't think i should be doing results[0]. save as cls(results)?
    @classmethod
    def validate_email(cls, data):
        query = "SELECT email, password FROM users WHERE email = %(email)s;"

        modified_data = {
            'email': data['email']
        }

        connection = connectToMySQL('registration_schema')
        results = connection.query_db(query, modified_data)

        if len(results) < 1:
            flash("This email does not exist, try again.")
            return False

        return results[0]


    @staticmethod
    def validate_registration(user):
        is_valid = True
        # test whether a field matches the patterns defined above
        if not email_regex.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if not first_name.match(user['first_name']):
            flash("Invalid first name. First name must be letters between 2-45 characters long")
            is_valid = False
        if not last_name.match(user['last_name']):
            flash("Invalid Last name. Last name must be letters between 2-45 characters long")
            is_valid = False
        #make sure password is at least 8 characters long
        if len(user['password']) < 8:
            flash("Invalid password. Password must be a minimum of 8 alphanumeric characters and a maximum of 45 characters")
            is_valid = False
        #make sure password matches the confirm password
        if not user['password'] == user['confirm_password']:
            flash("Passwords do not match. Please enter again.")
            is_valid = False
        
        #make sure email is unique
        query = "SELECT email FROM users WHERE email = %(email)s;"
        modified_data = {
            'email': user['email']
        }
        connection = connectToMySQL('registration_schema')
        results = connection.query_db(query, modified_data)

        if len(results) > 0:
            is_valid = False
            flash("This email already exists. Please log in to continue.")

        return is_valid
        

