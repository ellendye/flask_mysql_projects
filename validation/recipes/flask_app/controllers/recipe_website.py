from werkzeug.utils import secure_filename
from flask_app import app

from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.users import User
from flask_app.models.recipes import Recipe


@app.route('/')
def index():
    #renders the login page. Can only see this page if not logged in. if user is logged in it directs to the dashboard
    if 'id' in session:
        return redirect('/dashboard')
    
    #renders the sign-in/sign-up page
    return render_template("index.html")


#method to validate the login and registration
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
        #set user_in_db to the validate_email function. check to see if email exists. if not, redirect back to page w flash message
        user_in_db = User.validate_email(request.form)
        if not user_in_db:
            return redirect('/')
        #check to see if the password from the user matches the password from the request form using the bcrypt
        if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        # if we get False after checking the password send this flash message and redirect to homepage
            flash("Invalid Password. Please enter again")
            return redirect('/')
    
    #set user to the get_user function from model
    user = User.get_user(request.form)

    #set session at 'id' and 'first_name' to be the logged in user's first name and id
    
    session['id'] = user['id']
    session['first_name'] = user['first_name']

    #redirect to the success page
    return redirect('/dashboard')



#dashboard - can only see if user is logged in
@app.route('/dashboard')
def show_user():
    if not 'id' in session:
        flash("Please log in")
        return redirect('/')
    # renders the log in page. 

    #gets all the recipes from the database
    recipes = Recipe.get_all_recipes()
    return render_template("logged_in.html", recipes=recipes)


#create recipe page. can only see if user is not logged in
@app.route('/recipes/new')
def new_recipe():
    if not 'id' in session:
        flash("Please log in")
        return redirect('/')

    return render_template("create.html")

#method to submit the recipe
@app.route('/recipes/new/submit', methods=['POST'])
def create_new_recipe():
    
    #validate the recipe requirements
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    #classmethod to create a new recipe
    Recipe.create_new_recipe(request.form, session['id'])

    return redirect('/dashboard')

#classmethod to view a specific recipe. can only be viewed if user is logged in
@app.route('/recipes/<int:id>')
def show_recipe(id):
    if not 'id' in session:
        flash("Please log in")
        return redirect('/')

    recipe = Recipe.get_recipe(id)


    return render_template("show.html", recipe=recipe)

#class method to edit a recipe. can only be edited if user is logged in and if session id == recipe user_id
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not 'id' in session: 
        flash("Please log in")
        return redirect('/')

    recipe = Recipe.get_recipe(id)
    
    if session['id'] != recipe['user_id']:
        return redirect('/')

    return render_template("edit.html", recipe=recipe)

#classmethod to submit a recipe that was edited. validates per the wireframe rules. redirects to dashboard per the wireframe.
@app.route('/recipes/edit/<int:id>/submit', methods=['POST'])
def edit_recipt_submit(id):

    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')

    Recipe.edit_recipe(request.form, id)

    return redirect("/dashboard")

#class method to delete a recipe. can only delete a recipe if the session id and user id(/creator of recipe) are the same.
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):

    if not 'id' in session: 
        flash("Please log in")
        return redirect('/')

    recipe = Recipe.get_recipe(id)

    if session['id'] != recipe['user_id']:
        return redirect('/')

    Recipe.delete_recipe(id)

    return redirect('/')

@app.route('/logout')
def log_out_user():

    #clears the session. only logs out user if you go through this route. redirects back to the home page.
    session.clear()

    return redirect('/')