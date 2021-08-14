from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
from flask import app, flash

class Recipe: 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_thirty_mins = data['under_thirty_mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    #method to get all recipes in database
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"

        connection = connectToMySQL('recipe_schema')
        results = connection.query_db(query)

        recipes = []
        for result in results: 
            recipes.append(cls(result))
    
        return recipes

    #method to create a new recipe
    @classmethod
    def create_new_recipe(cls, data, id):
        query = "INSERT INTO recipes (name, description, instructions, date_made_on, under_thirty_mins, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made_on)s, %(under_thirty_mins)s, %(user_id)s);"
        
        modified_data = {
            'name': data['name'],
            'description': data['description'],
            'instructions': data['instructions'],
            'date_made_on': data['date_made_on'],
            'under_thirty_mins': data['under_thirty_mins'],
            'user_id': id
        }

        connection = connectToMySQL('recipe_schema')
        results = connection.query_db(query, modified_data)
        
        return results

    #method to get a specific recipe 
    @classmethod
    def get_recipe(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"

        modified_data = {
            'id': id
        }

        connection = connectToMySQL("recipe_schema")
        results = connection.query_db(query,modified_data)

        if len(results) == 0:
            return None

        return cls(results[0])
    
    #method to edit a specific recipe
    @classmethod
    def edit_recipe(cls, data, id):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made_on = %(date_made_on)s, under_thirty_mins = %(under_thirty_mins)s WHERE id = %(id)s;"

        modified_data = {
            'id': id,
            'name': data['name'],
            'description': data['description'],
            'instructions': data['instructions'],
            'date_made_on': data['date_made_on'],
            'under_thirty_mins': data['under_thirty_mins']
        }


        connection = connectToMySQL("recipe_schema")
        results = connection.query_db(query,modified_data)

        return results

    #method to delete a specific recipe
    @classmethod
    def delete_recipe(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        modified_data = {
            'id': id
        }

        connection = connectToMySQL("recipe_schema")
        results = connection.query_db(query,modified_data)

        return results


    #method to validate a recipe based off of wireframe. Recipe name, description and instructions must all be at least 3 characters long. Apply validation when editing and creating.
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        # test whether a field matches the patterns defined above
        if len(recipe['name']) < 3:
            flash("Invalid recipe name. Name must be at least three characters")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Invalid recipe description. Description must be at least three characters long")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Invalid recipe instructions. Instructions must be at least three characters")
            is_valid = False
        if len(recipe['date_made_on']) < 1:
            flash("Invalid recipe date. Date created must be selected")
            is_valid = False


        return is_valid