# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users
            
    @classmethod
    def create_users(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the create_user method from users.py controller
        modified_data = {
            'first_name': data['fname'],
            'last_name': data['lname'],
            'email': data['email']
        }
        connection = connectToMySQL('users_schema')
        results = connection.query_db(query, modified_data)
        return results
    
    @classmethod
    def get_user(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        data = {
            'id': id
        }
        connection = connectToMySQL('users_schema')
        results = connection.query_db(query, data)
        user = results[0]
        return user

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM users WHERE ( id = %(id)s);"

        data = {
            'id': id
        }
        # passing in the ID from the delete functino on users.py controller. using that id to execute query.
        return connectToMySQL('users_schema').query_db( query, data )

    @classmethod
    def update(cls, data, id ):
        query = "UPDATE users SET first_name = %(fname)s , last_name = %(lname)s , email = %(email)s , updated_at = NOW() WHERE id = %(id)s;"
        # data is the request.form that will be passed into the update method from users.py controller
        modified_data = {
            "id": id,
            "fname": data['fname'],
            "lname" : data["lname"],
            "email" : data["email"]
        }
        
        return connectToMySQL('users_schema').query_db( query, modified_data )