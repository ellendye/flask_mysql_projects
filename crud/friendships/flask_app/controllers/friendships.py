from flask_app import app

from flask import render_template, redirect, session, request

from flask_app.models.users import User#name of model file# import #name of class#


@app.route("/")
def index():
    # redirecting to the /users location per the wireframe
    return redirect("/friendships")

@app.route("/friendships")
def show_frienships():
    # renders the index.html. sends in all friendships and users to display
    
    friendships = User.get_all_friendships()
    users = User.get_all()
    return render_template("index.html", friendships = friendships, users = users)

@app.route("/friendships/adduser", methods = ['POST'])
def add_user():
    #calls on the add user method from the user class. adds user into system

    User.create_new_user(request.form)
    return redirect('/')

@app.route("/friendships/create", methods = ['POST'])
def create_friendship():
    #calls on the create frienship method from the user class. adds frienship into system. 
    print(request.form)
    User.create_friendship(request.form)
    return redirect('/')