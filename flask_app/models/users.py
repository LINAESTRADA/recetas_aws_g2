from flask_app.config.mysqlconnection import connectToMySQL

import re # re expersion regular son reglas para determinada palabara porejemplo plabras con mayusculas y minusculas o numeros esto va a crear un patron que se cumpla o que no se cumpla
#expresion regular de email siempre va a ser la misma lo basico es un patron 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')#este es el patron


from flask import flash #flash despliega mensajes de error al usuario

class User:

    def __init__(self, data):
        self.id  = data['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data ['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result

    @staticmethod
    def valida_usuario(formulario):

        es_valido = True
        #aqui validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe de tener al menos 3 carateres', 'registro')
            es_valido = False

        if len(formulario['last_name']) < 3:
            flash('Apellido debe de tener al menos 3 caracteres', 'registro')
            es_valido = False

        #aqui verificamos que el email tenga un formato correcto
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail invalido', 'registro')
            es_valido = False

        #aqui que el password tiene 6 caracteres
        if len(formulario['password']) < 6:
            flash('contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False

        #verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            flash('contraseña no coinciden', 'registro')
            es_valido = False

        #consultar si ya existe ese correo electronico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recetas').query_db(query, formulario)
        if len(results) >=1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False
 
        return es_valido 

    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        #yo aqui voy a recibir una lista
        result = connectToMySQL('recetas').query_db(query, formulario) #los select regresan una lista
        if len(result) < 1: #esto sigfica que no existe ese correo 
            return False
        else:
            user = cls(result[0])
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        user = cls(result[0])
        return user
