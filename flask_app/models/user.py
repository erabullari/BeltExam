from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    db_name = "exam_db"
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (firstName, lastName, email, password) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users where users.email=%(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users 
    
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users where id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_user_info_by_email(cls,data):
        query = "SELECT * FROM users where users.email=%(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET firstName=%(firstName)s, lastName=%(lastName)s, email=%(email)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    

#validimi per user
    @staticmethod
    def validate_user(user):
        is_valid = True
        data = {
            'email': user['email']
        }
        if User.get_user_by_email(data):
            flash("Email already in use.","emailError")
            is_valid = False
        if len(user['firstName']) < 2:
            flash("First name must be at least 2 characters.","firstNameError")
            is_valid = False
        if len(user['lastName']) < 2:
            flash("Last name must be at least 2 characters.","lastNameError")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is required.","emailError")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.","passwordError")
            is_valid = False
        if user['password'] != user['confirmpassword']:
            flash("Passwords do not match.","passwordError")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_updated_user(user):
        is_valid = True
       
        data = {
            'email': user['email'],
            'id': session['user_id']
        }

        user_in_db = User.get_user_by_email(data)
        
        if user_in_db and user_in_db['id'] != int(data['id']):
            flash("Email already in use.","emailError")
            is_valid = False
        if len(user['firstName']) < 2:
            flash("First name must be at least 2 characters.","firstNameError")
            is_valid = False
        if len(user['lastName']) < 2:
            flash("Last name must be at least 2 characters.","lastNameError")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is required.","emailError")
            is_valid = False
            return is_valid
    
    