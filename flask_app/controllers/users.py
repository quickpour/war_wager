from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# this is just testing now
@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route('/')
def testing():
    return render_template('testing.html')


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
    person = user.User.get_user_by_id(session)
    return render_template('/testing_success.html', person=person)


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/validate_login', methods=['POST'])
def validate_logging():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    checkee = user.User.get_user_by_email(data)
    if not checkee:
        flash("Please input a valid email!", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(checkee.password, request.form['password']):
        flash("Please input a valid password!", "login")
        return redirect('/')
    session['id'] = checkee.id
    print(session)
    print("it has made it to the end of validate_logging in users.py")
    return redirect('/user_success')
