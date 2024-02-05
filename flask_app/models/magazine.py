from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Magazine:
    db_name = "exam_db"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @staticmethod
    def validate_magazine(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Name must be at least 3 characters.",'titleError')
            is_valid = False
        if len(data['description']) < 10:
            flash("Description must be at least 10 characters.",'descriptionError')
            is_valid = False
        if Magazine.check_magazine_by_title(data):
            flash("Magazine already exists.",'titleError')
            is_valid = False
        return is_valid
    


    @classmethod
    def check_magazine_by_title(cls, data):
        query = "SELECT * FROM magazines WHERE title=%(title)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return True
        return False
    @classmethod
    def save_magazine(cls,data):
        query = "INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    
    @classmethod
    def get_all_magazines(cls):#all magazines and user with id
        query = "SELECT * FROM magazines LEFT JOIN users ON magazines.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        magazines = []
        if results:
            for magazine in results:
                magazines.append(magazine)
            return magazines
        return magazines
    
    @classmethod
    def get_magazine_by_id(cls, data):#all magazines and user with  specific id
        query = "SELECT * FROM magazines LEFT JOIN users ON magazines.user_id = users.id WHERE magazines.id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM magazines WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    

    #extra 
    #subscription 

    @classmethod
    def subscribe(cls, data):
        query = "INSERT INTO subcribes (user_id, magazine_id) VALUES (%(user_id)s, %(magazine_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def controlle(cls, data):
        query = "SELECT * FROM subcribes WHERE user_id=%(user_id)s AND magazine_id=%(magazine_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return True
        return False
    
    @classmethod
    def all_subscribed(cls, data):
        query = "SELECT * FROM subcribes LEFT JOIN magazines ON subcribes.magazine_id = magazines.id LEFT JOIN users ON subcribes.user_id = users.id WHERE magazines.id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        subscribed = []
        if results:
            for sub in results:
                subscribed.append(sub)
            return subscribed
    
    @classmethod
    def get_all_subscriptions(cls, data):
        query = "SELECT * FROM subcribes LEFT JOIN magazines ON subcribes.magazine_id = magazines.id LEFT JOIN users ON subcribes.user_id = users.id WHERE subcribes.user_id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        subscribed = []
        if results:
            for sub in results:
                subscribed.append(sub)
            return subscribed
        return subscribed
    
    
    
    @classmethod
    def deletesub(cls, data):
        query = "DELETE FROM subcribes WHERE user_id=%(user_id)s AND magazine_id=%(magazine_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
        
        
    @classmethod
    def get_sub_for_each_magazine(cls, data):
        query = "SELECT * FROM subcribes;"
        result= connectToMySQL(cls.db_name).query_db(query, data)
        number = []
        if result:
            for sub in result:
                number.append(sub)
            return number
    
   
    
        
    
    
        