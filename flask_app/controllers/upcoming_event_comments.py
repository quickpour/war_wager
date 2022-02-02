from flask_app import app
from flask import request, render_template, redirect, session
from flask_app.models import upcoming_event_comment

@app.route('/create_new_comment', methods=['POST'])
def new_comment_create():
    print("we are here ***************************")
    upcoming_event_id = request.form['upcoming_event_id']
    if 'id' not in session:
        return redirect('/')
    if not upcoming_event_comment.Upcoming_event_comment.validate_comment(request.form):
        return redirect(f'/view_event_secure/{upcoming_event_id}')
    data = {
        'comment' : request.form['comment'],
        'user_id' : session['id'],
        'upcoming_event_id' : request.form['upcoming_event_id']
    }
    upcoming_event_comment.Upcoming_event_comment.create_comment(data)
    return redirect(f'/view_event_secure/{upcoming_event_id}')

@app.route('/comment_editor', methods=["POST"])
def comment_index():
    if 'id' not in session:
        return redirect('/')
    upcoming_event_id = request.form['upcoming_event_id']
    print("****** we made it past boys **************")
    upcoming_event_comment.Upcoming_event_comment.update_comment_actually(request.form)
    return redirect(f'/view_event_secure/{upcoming_event_id}')

@app.route('/delete_comment_user', methods=['POST'])
def delete_comment():
    if 'id' not in session:
        return redirect('/')
    event_id = request.form['upcoming_event_id']
    upcoming_event_comment.Upcoming_event_comment.delete_comment(request.form)
    return redirect(f'/view_event_secure/{event_id}')
