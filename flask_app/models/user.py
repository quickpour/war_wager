from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.past_events = []
        self.upcoming_events = []
    db = "WarWager" 

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(data):
        is_true = True
        if len(data['first_name']) < 2:
            flash("First Name must be at leaset 2 characters!", "register")
            is_true = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters!", "register")
            is_true = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please enter a valid email", "register")
            is_true = False
        if User.get_user_by_email(data):
            flash("email is already taken!", "register")
            is_true = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long!" , "register")
            is_true = False
        if data['password'] != data['pw_confirm']:
            flash("Passwords dont match!", "register")
            is_true = False
        return is_true
        


