from asyncio import events
from flask import session, flash
from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL

class Upcoming_event:
    def __init__(self, data):
        self.id = data['id']
        self.game = data['game']
        self.name = data['name']
        self.date = data['date']
        self.time = data['time']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.comments = []
    db = "WarWager"

    @staticmethod
    def validate_upcoming_event(data):
        is_true = True
        if len(data['game']) < 1:
            flash("Please enter a valid game!", "upcoming_event")
            is_true = False
        if len(data['name']) < 2:
            flash("Please enter a valid event name!", "upcoming_event")
            is_true = False
        if len(data['date']) < 1:
            flash("Please enter a valid date!", "upcoming_event")
            is_true = False
        if len(data['time']) < 1:
            flash("Please enter a valid time!", "upcoming_event")
            is_true = False
        if len(data['description']) < 2:
            flash("Please enter a description", "upcoming_event")
            is_true = False
        return is_true

    @classmethod
    def create_upcoming_event(cls, data):
        query = "INSERT INTO upcoming_events (game, name, date, time, description, created_at, updated_at, user_id) VALUES (%(game)s, %(name)s, %(date)s, %(time)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_upcoming_by_game(cls, data):
        query = "SELECT * FROM upcoming_events LEFT JOIN users ON upcoming_events.user_id = users.id WHERE game = %(game)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        upcoming_events = []
        for event in results:
            event_data = {
                'id' : event['id'],
                'game' : event['game'],
                'name' : event['name'],
                'date' : event['date'],
                'time' : event['time'],
                'description' : event['description'],
                'created_at' : event['created_at'],
                'updated_at' : event['updated_at']
            }
            single_event = cls(event_data)
            user_data = {
                'id' : event['users.id'],
                'first_name' : event['first_name'],
                'last_name' : event['last_name'],
                'email' : event['email'],
                'password' : event['password'],
                'created_at' : event['users.created_at'],
                'updated_at' : event['users.updated_at']
            }
            single_user = user.User(user_data)
            single_event.creator = single_user
            upcoming_events.append(single_event)
        return upcoming_events

    @classmethod
    def get_upcoming_by_id(cls, id):
        data = {
            'id' : id
        }
        query = "SELECT * FROM upcoming_events LEFT JOIN users ON upcoming_events.user_id = users.id WHERE upcoming_events.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        event_data = {
                'id' : results[0]['id'],
                'game' : results[0]['game'],
                'name' : results[0]['name'],
                'date' : results[0]['date'],
                'time' : results[0]['time'],
                'description' : results[0]['description'],
                'created_at' : results[0]['created_at'],
                'updated_at' : results[0]['updated_at']
            }
        upcoming_event = cls(event_data)
        user_data = {
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }
        author = user.User(user_data)
        upcoming_event.creator = author
        return upcoming_event

    @classmethod
    def update_upcoming_event(cls, data):
        query = "UPDATE upcoming_events SET game = %(game)s, name = %(name)s, date=%(date)s, time=%(time)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_upcoming_event(cls, data):
        query = "DELETE FROM upcoming_events WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)