from flask_app import app

from flask import render_template, redirect, session, request

from flask_app.models.dojos import Dojo
from flask_app.models.ninjas import Ninja

@app.route("/")
def index():
    # redirecting to the /users location per the wireframe
    return redirect("/dojos")

@app.route("/dojos")
def show_dojo():
    # renders the dojo.html and shows all dojos
    dojos = Dojo.get_all()
    return render_template("dojo.html", dojos=dojos)

@app.route("/dojos/create", methods=['POST'])
def create_dojo():
    # calling on the create_dojo method from the Dojo class and redirecting to Dojo page to show list of Dojos
    Dojo.create_dojo(request.form)
    return redirect("/dojos")

@app.route("/dojos/<int:dojo_id>")
def view_ninjas_at_dojo(dojo_id):
    #redirects to the show_dojo.html page and calls/returns the get_all_from_dojo method in Ninja model
    ninjas = Ninja.get_all_from_dojo(dojo_id)
    dojo = Dojo.get_dojo(dojo_id)
    return render_template("show_dojo.html", ninjas = ninjas, dojo=dojo)

@app.route("/ninjas")
def render_ninja_form():
    # renders the ninja.html
    dojos = Dojo.get_all()
    return render_template("ninja.html", dojos = dojos)

@app.route("/ninja/create", methods=['POST'])
def create_ninja():
    # calling on the create_ninja method from the Nina class and redirecting to home page to show list of Dojos
    Ninja.create_ninja(request.form)
    return redirect("/dojos")
