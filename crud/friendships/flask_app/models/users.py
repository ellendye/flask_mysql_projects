# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import friend
# model the class after the friend table from our database


class User: 
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friend = None

    @classmethod
    def get_all_friendships(cls):
        query = "SELECT * FROM users JOIN friendships ON users.id = friendships.user_id JOIN users as users2 ON user_id1 = users2.id;"

        connection = connectToMySQL('friendships_schema')
        results = connection.query_db(query)

        friendships = []
        for result in results:
            friend_info ={
                'id': result['users2.id'],
                'first_name': result['users2.first_name'],
                'last_name': result['users2.last_name'],
                'created_at': result['users2.created_at'],
                'updated_at': result['users2.updated_at']
            }
            user = cls(result)
            user.friend = friend.Friend(friend_info)
            friendships.append(user)
        print(friendships)

        return friendships
    
    @classmethod
    def create_new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, NOW(), NOW());"
        
        modified_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }

        connection = connectToMySQL('friendships_schema')
        results = connection.query_db(query, modified_data)
        #inserting form data into a modified query and sending them to the system

        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        connection = connectToMySQL('friendships_schema')
        results = connection.query_db(query)

        users = []
        for result in results:
            users.append( cls(result) ) 
        return users

    @classmethod
    def create_friendship(cls, data):
        query = "INSERT INTO friendships (user_id, user_id1, created_at, updated_at) VALUES (%(user_id)s, %(friend_id)s, NOW(), NOW());"

        modified_data = {
            'user_id': data['user_id'],
            'friend_id': data['friend_id']
        }

        connection = connectToMySQL('friendships_schema')
        results = connection.query_db(query, modified_data)

        return results