from flask import Flask, render_template, request, redirect, session, flash
from bcrypt_app import app
from bcrypt_app.models import userModel
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt(app)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def index():
    isLogged = False

    if 'userId' in session:
        isLogged = True
        return redirect('/dashboard')

    return render_template("index.html", isLogged = isLogged)

@app.route('/register', methods=['POST'])
def register():
    if not userModel.User.validateRegister(request.form):
        return redirect('/')
    
    encryptedPassword = bcrypt.generate_password_hash(request.form['password'])

    gender = request.form['gender']
    
    if gender == 'Self describe':
        gender = request.form['other']

    data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'email': request.form['email'],
        'password': encryptedPassword,
        'gender': gender,
        'birthday': request.form['birthday']
    }

    print(request.form['birthday'])
    today = datetime.now()

    result = userModel.User.save(data)

    if type (result) is int and result > 0:
        session['userId'] = result
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    if not userModel.User.validateLogin(data):
        return redirect('/')

    user = userModel.User.findUserByEmail(data)

    if user != None:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Invalid Email / Password', 'login_error')
            return redirect('/')
    
        session['userId'] = user.id
        return redirect('/dashboard')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    userId = None

    if 'userId' in session:
        userId = session['userId']
        user = userModel.User.findUserById({'userId': userId})
        isLogged = True
        return render_template('dashboard.html', user = user, isLogged = isLogged)
    else:
        return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')
