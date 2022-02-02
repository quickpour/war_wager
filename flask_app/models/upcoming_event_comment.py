from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
from flask_app.models import user

class Upcoming_event_comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.upcoming_event_id = data['upcoming_event_id']
        self.author = None
    db = "WarWager"

    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO upcoming_event_comments (comment, user_id, upcoming_event_id, created_at, updated_at) VALUES (%(comment)s, %(user_id)s, %(upcoming_event_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_comment(data):
        is_true = True
        if len(data["comment"]) < 2:
            flash("Please enter a valid comment!", "comment")
            is_true = False
        return is_true

    @classmethod
    def get_upcoming_event_comments(cls, data):
        print("i hope this will appear")
        query = "SELECT * FROM upcoming_event_comments LEFT JOIN users on users.id = upcoming_event_comments.user_id WHERE upcoming_event_comments.upcoming_event_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        all_comments = []
        for result in results:
            comment_data = {
                'id' : result['id'],
                'comment' : result['comment'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'upcoming_event_id' : result['upcoming_event_id'],
                'user_id' : result['user_id']
            }
            the_comment = cls(comment_data)
            user_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' :result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }
            the_comment.author = user.User(user_data)
            all_comments.append(the_comment)
        return all_comments

    @classmethod
    def update_comment_actually(cls, data):
        query = "UPDATE upcoming_event_comments SET comment = %(comment)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM upcoming_event_comments WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)