from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user

#this is just testing now
@app.route('/')
def landing():
    return render_template('testing.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    print("lets try this again")
    if not user.User.validate_register(request.form):
        return redirect('/')
    return redirect('/')