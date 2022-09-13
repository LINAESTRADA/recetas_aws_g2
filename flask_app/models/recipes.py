from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = ['user_id']

        #LEFT JOIN
        self.first_name = data['first_name']

    @staticmethod
    def valida_receta(formulario):
        es_valido = True

        if len(formulario['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False

        if len(formulario['description']) < 3:
            flash('La descripcion de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False

        if len(formulario['instructions']) < 3:
            flash('Las  instrucciones de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False

        if formulario['date_made'] == "":
            flash('ingrese una fecha', 'receta')
            es_valido = False

        return es_valido 

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, %(user_id)s)"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recetas').query_db(query) #Lista de diccionarios 
        recipes = []
        for recipe in results:
            #recipe = diccionario
            recipes.append(cls(recipe)) #1.- cls(recipe) me crea una instancia en base al diccionario, 2.- Agrego la instancia a mi lista de recetas

        return recipes

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        recipe = cls(result[0])
        return recipe 

    @classmethod
    def update(cls, formulario):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under30=%(under30)s WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result