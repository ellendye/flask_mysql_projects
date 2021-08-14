from flask_app.config.mysqlconnection import connectToMySQL


class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # calling on the dojos table and returning all columns

        connection = connectToMySQL('dojos_and_ninjas_schema')
        results = connection.query_db(query)
        # setting connection to the schema in MySQL. setting results to the query that was just called

        dojos = []
        for result in results:
            dojos.append( cls(result) )
            #going through the results found from the query and setting them into an array. Array will be an array of dictionaries. returning the results below
        return dojos
    
    @classmethod
    def create_dojo(cls, data):
        query = "INSERT INTO dojos (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        #calling the query to add in a new dojo from the dojos table

        modified_data = {
            'name': data['dojo_name']
        }
        #setting modified data to the new dojo name
        
        connection = connectToMySQL('dojos_and_ninjas_schema')
        results = connection.query_db(query, modified_data)
        # setting connection to the schema in MySQL. setting results to the query that was just called and returning thos results

        return results

    @classmethod
    def get_dojo(cls, id):
        query = "SELECT * FROM dojos WHERE id = %(id)s;"
        data = {
            'id': id
        }
        connection = connectToMySQL('dojos_and_ninjas_schema')
        results = connection.query_db(query, data)
        dojo = results[0]
        return dojo

