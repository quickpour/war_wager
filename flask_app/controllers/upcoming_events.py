from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import upcoming_event, user


@app.route('/upcoming_event/creation', methods=['POST'])
def create_event():
    if 'id' not in session:
        return redirect('/')
    if not upcoming_event.Upcoming_event.validate_upcoming_event(request.form):
        return redirect('/to_event_create')
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
    return render_template('upcoming_battles_list.html', game=game, upcoming_events=upcoming, user=person)

@app.route('/upcoming/nolog/<string:game>')
def upcoming_by_game_nolog(game):
    print("i am attempting to print", game)
    data = {
        "game" : game
    }
    upcoming = upcoming_event.Upcoming_event.get_upcoming_by_game(data)
    return render_template('nolog_upcoming_list.html', game=game, upcoming_events=upcoming)

@app.route('/view_event_secure/<int:id>')
def get_upcoming_event_by_id(id):
    upcoming_battle = upcoming_event.Upcoming_event.get_upcoming_by_id(id)
    person = user.User.get_user_by_id(session)
    return render_template('upcoming_battle_event.html', upcoming_battle=upcoming_battle, person=person)

@app.route('/view_event_secure/nolog/<int:id>')
def get_upcoming_event_by_id_nolog(id):
    upcoming_battle = upcoming_event.Upcoming_event.get_upcoming_by_id(id)
    return render_template('nolog_upcoming_event.html', upcoming_battle=upcoming_battle)

@app.route('/to_event_create')
def event_creation():
    if 'id' not in session:
        return redirect('/')
    person = user.User.get_user_by_id(session)
    return render_template('upcoming_battle_create.html', person=person)

@app.route('/edit_upcoming_event/<int:id>')
def to_event_edit(id):
    the_event = upcoming_event.Upcoming_event.get_upcoming_by_id(id)
    return render_template('edit_upcoming_battle.html', event=the_event)

@app.route('/edit_the_event', methods=['POST'])
def edit_upcoming_e():
    if 'id' not in session:
        return redirect('/')
    upcoming_event.Upcoming_event.update_upcoming_event(request.form)
    the_id = request.form['id']
    return redirect(f'/view_event_secure/{the_id}')

@app.route('/delete_upcoming/<int:id>')
def delete_upcoming(id):
    data = {
        'id' : id
    }
    upcoming_event.Upcoming_event.delete_upcoming_event(data)
    return redirect('/user_success')