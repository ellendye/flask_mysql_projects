from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.users import User

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/wall')
    #renders the home page. two different pages based on if it's logged in or not per the HTML
    return render_template("index.html")

@app.route('/validate', methods=['POST'])
def validate_and_login():

    #if the request.form is coming from registration, do this block
    if request.form['which_form'] == 'registration':
        #do the registration check. check for valid first name, last name, email, if email already exists, if passwords are valid and if they match
        if not User.validate_registration(request.form):
            #if registration form is NOT valid, redirect to the home page and show flash messaging
            return redirect('/')
        #hash password before it's stored in system
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        
        #set the data to send to the database
        data = {
            "first_name": request.form['first_name'], 
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash
        }
        #insert into the database
        User.save_information(data)

    #if the request.form is coming from login, do this block
    elif request.form['which_form'] =='login':
        #set user_in_db to the validate_email function. check to see if email exists. if not, redirect w flash message
        user_in_db = User.validate_email(request.form)
        if not user_in_db:
            return redirect('/')
        #check to see if the password frmo the user matches the password from the request form using the bcrypt
        if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        # if we get False after checking the password send this flash message and redirect to homepage
            flash("Invalid Password. Please enter again")
            return redirect('/')
    
    #set user to the get_user function from model
    user = User.get_user(request.form)

    #should not be able to access a new request form if user is not logged out but set this just in case? take this check out? 
    if not 'id' in session:
        # should there be anything else saved in session? just this for now? or do i need less? 
        session['id'] = user['id']
        session['first_name'] = user['first_name']
        session['logged_in'] = True

    #redirect to the wall page
    return redirect('/wall')


@app.route('/wall')
def show_user():
    if not 'id' in session:
        return redirect('/')
    # renders the log in page.
    
    new_messages = User.get_user_messages(session['id'])
    num_messages_sent = User.get_num_messages_sent(session['id'])
    other_users=User.get_other_users(session['id'])
    num_messages_received = User.get_num_messages_received(session['id'])
    return render_template("logged_in.html", other_users=other_users, num_messages_sent = num_messages_sent, new_messages=new_messages, num_messages_received=num_messages_received)

@app.route('/wall/add_message', methods=['POST'])
def add_message():

    modified_data = {
        'current_user_id': session['id'], 
        'receiver_id': request.form['id'],
        'message': request.form['message']
    }
    if not User.validate_message(request.form): 
        return redirect('/')

    User.send_message(modified_data)

    return redirect('/wall')

@app.route('/wall/delete_message/<int:id>')
def delete_message(id):

    User.delete_message(id)

    return redirect('/wall')

@app.route('/logout')
def log_out_user():

    #clears the session. only logs out user if you go through this route. redirects back to the home page.
    session.clear()

    return redirect('/')