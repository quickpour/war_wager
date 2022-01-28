from flask import session, flash

from flask_app.config.mysqlconnection import connectToMySQL

class upcoming_event:
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