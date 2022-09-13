from flask_app import app

#Importando mi controlador
from flask_app.controllers import users_controller, recipes_controller

#pipenv install flask pymysql flask-bcrypt
#pipenv shell
#python server.py

if __name__=="__main__":
    app.run(debug=True)


#pipenv lock -r > requirements.txt
#https://www.toptal.com/developers/gitignore

#git bash
#git init
#git add .
