from flask_app import app

from flask import render_template, redirect, session, request

from flask_app.models.users import User


@app.route("/")
def index():
    # redirecting to the /users location per the wireframe
    return redirect("/users")


@app.route('/users')
def read_all_users():
    #sets users to users get all so that we can go through the document and create a table of all users
    users = User.get_all()
    return render_template("index.html", all_users = users)


@app.route('/users/new')
def add_new_user():
    #rendering create page
    return render_template('create.html')


@app.route('/users/new/add',methods=["POST"])
def create_user():
    #sending all information from the request.form to a User method called create user and redirecting to the homepage
    User.create_users(request.form)
    return redirect('/')


@app.route("/users/<int:id>")
def show_user(id):
    # rendering the template for the show user page. Call on the get_user method from the User model to get that users information
    user = User.get_user(id)
    return render_template("show.html", user_info = user)


@app.route("/users/<int:id>/edit")
def edit_user(id):
    # rendering the template for the show user page
    users = User.get_user(id)
    return render_template("edit.html", user_info = users)


@app.route('/users/edit/<int:id>/update',methods=["POST"])
def edit_user_update(id):
    #sending all the info from the request.form to a User method called update. Redirecting back to show user page after complete
    User.update(request.form, id)
    return redirect(f'/users/{id}')

@app.route('/delete/<int:id>')
def delete_user(id):
    User.delete(id)
    return redirect('/')