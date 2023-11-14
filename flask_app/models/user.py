from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "users_reg_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
            """
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_user(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
            """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def unique_email(cls):
        query = "SELECT email FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        emails = []
        for email in results:
            emails.append(email['email'])
        return emails

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("First name cannot be blank", 'reg')
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name cannot be blank", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format", 'reg')
            is_valid = False
        if user['email'] in User.unique_email():
            flash("Email already being used", 'reg')
            is_valid = False
        if re.search('[0-9]', user['password']) is None:
            flash("Password must contain a number", 'reg')
            is_valid = False
        if re.search('[A-Z]', user['password']) is None:
            flash("Password must contain a capital letter", 'reg')
            is_valid = False
        if user['password'] != user['con_password']:
            flash("Passwords must match", 'reg')
            is_valid = False
        return is_valid