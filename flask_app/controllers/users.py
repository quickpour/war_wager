from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# this is just testing now
@app.route('/testing')
def testing():
    return render_template('testing.html')


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/register')
def register_page():
    return render_template('registration.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    print("lets try this again")
    if not user.User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    index = user.User.register_user(data)
    session['id'] = index
    print(session['id'], "this is it loggins")
    return redirect('/user_success')


@app.route('/user_success')
def valid_user():
    return render_template('/testing_success.html')

@app.route('/login')
def login_page():
    return render_template('/login.html')
