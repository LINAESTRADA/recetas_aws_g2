#esta inicializa nuestra aplicacion 

from flask import Flask

app = Flask(__name__)

#establecemos una secret key aqui debajo 
app.secret_key = "Mi llave super secreta" #nos da un grado de seguridad o encriptacion