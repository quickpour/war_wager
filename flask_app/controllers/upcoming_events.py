from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import upcoming_event, user


@app.route('/upcoming_event/creation', methods=['POST'])
def create_event():
    if not upcoming_event.Upcoming_event.validate_upcoming_event(request.form):
        return redirect('/user_success')
    upcoming_event.Upcoming_event.create_upcoming_event(request.form)
    return redirect('/user_success')

@app.route('/upcoming/<string:game>')
def upcoming_by_game(game):
    print("i am attempting to print", game)
    data = {
        "game" : game
    }
    person = user.User.get_user_by_id(session)
    upcoming = upcoming_event.Upcoming_event.get_upcoming_by_game(data)
    return render_template('testing_upcoming_display.html', game=game, upcoming_events=upcoming, user=person)

