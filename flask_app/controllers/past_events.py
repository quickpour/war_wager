from flask_app import app
from flask import render_template, redirect, session
from flask_app.models.user import User

@app.route('/past_events')
def past_events():
    if 'id' not in session:
        return redirect('/')
    person = User.get_user_by_id(session)
    return render_template('past_events.html', person=person)