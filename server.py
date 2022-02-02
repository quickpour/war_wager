from flask_app import app
from flask_app.controllers import users, upcoming_events, upcoming_event_comments, past_events


if __name__=="__main__":
    app.run(debug=True)


