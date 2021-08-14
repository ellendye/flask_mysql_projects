from flask_app import app

from flask import render_template, redirect, session, request

from flask_app.models.emails import User


@app.route('/')
def index():

    return render_template("index.html")

@app.route('/validate', methods=['POST'])
def validate():
    
    if not User.validate_user(request.form):
        return redirect('/')

    
    User.save_information(request.form)
    return redirect('/success')

@app.route('/success/<int:id>/delete')
def delete(id):
    User.delete_email(id)
    return redirect('/success')

@app.route('/success')
def successful_email():
    emails = User.get_all()
    return render_template('success.html', emails = emails)
