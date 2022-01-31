from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash

class Past_event:
    db = "WarWager"
    def __init__(self, data):
        self.id = data['id']
        self.game = data['game']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM past_events JOIN users ON users.id = past_events.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        past_events = []
        for past_event in results:
            instance = cls(past_event)
            userinfo = {
                "id" : past_event['users.id'],
                "first_name" : past_event['first_name'],
                "last_name" : past_event['last_name'],
                "email" : past_event['email'],
                "password" : past_event['password'],
                "created_at" : past_event['users.created_at'],
                "updated_at" : past_event['users.updated_at']
            }
            instance.user = User(userinfo)
            past_events.append(instance)
        return past_events
    @staticmethod
    def validate(data):
        is_true = True
        if len(data['game']) < 1:
            flash("Please enter a valid game!", "past_event")
            is_true = False
        if len(data['name']) < 2:
            flash("Please enter a valid event name!", "past_event")
            is_true = False
        if len(data['date']) < 1:
            flash("Please enter a valid date!", "past_event")
            is_true = False
        if len(data['time']) < 1:
            flash("Please enter a valid time!", "past_event")
            is_true = False
        if len(data['description']) < 2:
            flash("Please enter a description", "past_event")
            is_true = False
        return is_true
    @classmethod
    def save(cls, data):
        query = "INSERT INTO past_events (game, name, description, created_at, updated_at, user_id) VALUES(%(game)s, %(name)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        past_event_id = connectToMySQL(cls.db).query_db(query, data)
        return past_event_id
    @classmethod
    def get(cls, data):
        query = "SELECT * FROM past_events JOIN users ON users.id = past_events.user_id WHERE past_events.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        past_event = result[0]
        instance = cls(past_event)
        userinfo = {
            "id" : past_event['users.id'],
            "first_name" : past_event['first_name'],
            "last_name" : past_event['last_name'],
            "email" : past_event['email'],
            "password" : past_event['password'],
            "created_at" : past_event['users.created_at'],
            "updated_at" : past_event['users.updated_at']
        }
        instance.user = User(userinfo)
        return instance
    @classmethod
    def remove(cls, data):
        query = "DELETE FROM past_events WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return
    @classmethod
    def update(cls, data):
        query = "UPDATE past_events SET game = %(game)s, name = %(name)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        past_event = connectToMySQL(cls.db).query_db(query, data)
        return past_event