#copie y pegue estas tres lineas de user controller
from flask import render_template, redirect, session, request, flash
from flask_app import app

#aqui hacemos la importacion del modelo
from flask_app.models.users import User #esta es la importacion del modelo
from flask_app.models.recipes import Recipe


@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session: # con esto comprobamos que el usuario haya iniciado sesion
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #instancia del usuario que inicio sesion

    return render_template('new_recipe.html', user=user)


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:  #comprobamos que el usuario haya iniciado session
        return redirect('/')

    if not Recipe.valida_receta(request.form): #llama a la funcion de valida_receta enviandole el formulario, comprueba que sea valido
        return redirect('/new/recipe')

    Recipe.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>') #atraves de la url recibimos el id de la receta
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)#instancia del usuario que inicio sesion

    #la instancia de la receta que queremos editar
    formulario_receta ={"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id'])

    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['user_id']
    }

    user = User.get_by_id(formulario)

    formulario_receta = { "id": id }
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user=user, recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session: #solo puede ver la pagina si ya inicio sesion
        return redirect('/')

    formulario = {"id": id}
    Recipe.delete(formulario)

    return redirect('/dashboard')