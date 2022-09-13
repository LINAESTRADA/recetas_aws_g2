from flask import render_template, redirect, session, request, flash, jsonify
from flask_app import app

#aqui hacemos la importacion del modelo
from flask_app.models.users import User #esta es ka importacion del modelo
from flask_app.models.recipes import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrate', methods=['POST'])
def registrate():
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) #aqui encriptamos el password del usuario 

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario)#yo aqui recibo el identificador de mi nuevo usuario

    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #aqui abajo vamos a verificar que el email si exista
    user = User.get_by_email(request.form) #aqui recibimos la instancia del usuario o falso

    if not user:
        #flash('E_mail no encontrado', 'login')
        #return redirect('/')
        return jsonify(message="E-mail no encontrado")

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        #flash('Password incorrecto', 'login')
        #return redirect('/')
        return jsonify(message="Password incorrecto")

    session['user_id'] = user.id

    #return redirect('/dashboard')
    return jsonify(message="correcto")



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)

    recipes = Recipe.get_all()
        
    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')