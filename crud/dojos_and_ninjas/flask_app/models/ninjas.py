from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import dojos

class Ninja():
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojos_id = data['dojos_id']
        self.dojos = None
    
    @classmethod
    def get_all_from_dojo(cls, id):
        query = "SELECT ninjas.id as id, first_name, last_name, age, ninjas.created_at as created_at, ninjas.updated_at as updated_at, dojos_id, dojos.id as dojo_id, name, dojos.created_at as dojos_created_at, dojos.updated_at as dojos_updated_at FROM ninjas LEFT JOIN dojos ON dojos.id = ninjas.dojos_id WHERE dojos.id = %(id)s;"
        #joining ninja and dojo table where id is equal to id selected
        data = {
            'id': id
        }
        connection = connectToMySQL('dojos_and_ninjas_schema')
        results = connection.query_db(query, data)
        ninjas = []
        for result in results:
            dojo_info = {
                'id': result['dojo_id'],
                'name': result['name'],
                'created_at': result['dojos_created_at'],
                'updated_at': result['dojos_updated_at']
            }
            ninja = cls(result)
            ninja.dojos = dojos.Dojo(dojo_info)
            ninjas.append(ninja)
            

        return ninjas

    @classmethod
    def create_ninja(cls, data):
        query = "INSERT INTO ninjas (first_name, last_name, age, created_at, updated_at, dojos_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, NOW(), NOW(), %(dojos_id)s);"
        #calling the query to add in a new ninja from the ninja table

        modified_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'age': data['age'],
            'dojos_id': data['dojos_id']
        }
        #setting modified data to the new ninja info
        
        connection = connectToMySQL('dojos_and_ninjas_schema')
        results = connection.query_db(query, modified_data)
        print(results)
        # setting connection to the schema in MySQL. setting results to the query that was just called and returning thos results

        return results