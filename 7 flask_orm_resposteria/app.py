from flask import Flask
from conexion_db import base_de_datos
# libreria para las variables de entorno de nuestra maquina
from os import environ
# libreria que permite usar las variables de entorno del archivo .env
from dotenv import load_dotenv
# libreria para usar arquitectura rest (controladores)
from flask_restful import Api
# para tener los permisos de los CORS como un autenticacion
from flask_cors import CORS

# import Models
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel
from models.preparacion import PreparacionModel
from models.receta_ingrediente import RecetaIngredienteModel
from models.log import LogModel

# import Controllers
from controllers.ingrediente import (IngredientesController,
                                     IngredienteController,
                                     FitroIngredientesController)
from controllers.receta import RecetasController
from controllers.receta_ingrediente import RecetaIngredientesController
from controllers.preparacion import PreparacionesController


# metodo que permite cargar todas las variables de entorno del file .env
load_dotenv()

# instanciamos la app
app = Flask(__name__)

# autenticacion de los CORS acceso permitido para las sgts metodos y dominios
CORS(app=app, methods=['GET', 'POST', 'PUT', 'DELETE'],
     origins='*', allow_headers='*')

api = Api(app=app)

#! area de configuracion
# 'mysql://root:root@localhost/reposteria'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')

# ?si es True SQLALChemy rastreara las modificaciones de los objetos(modelos) y lanzara senales de cambio, su valor predeterminado es None, igual habilita el tracking pero emite una advertencia que en futuras versiones se removera el valor x default None y si o si tendremos que indicar un valor inicial True o False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ?inicializa la conexion con la base de datos para darle las credenciales definidas en el app.config
base_de_datos.init_app(app)
# eliminar todas las tablas(antes de crear debes eliminar)
# base_de_datos.drop_all(app=app)
# crear todas las tablas
base_de_datos.create_all(app=app)


# todo:zona de enrutamiento
#read -- create
api.add_resource(IngredientesController, '/ingredientes')

# get -- put -- delete (1 ingrediente)
api.add_resource(IngredienteController, '/ingrediente/<int:id>')

# buscar 1 ingrediente
api.add_resource(FitroIngredientesController, '/buscar_ingrediente')

# get-post recetas
api.add_resource(RecetasController, '/recetas')

# add los ids de receta e ingrediente a la super tabla Receta_ingrediente
api.add_resource(RecetaIngredientesController, '/recetas_ingredientes')


# get - put - delete (1 receta) no se de donde es esto
# api.add_resource(RecetaController,/receta/<int:id>)

#
api.add_resource(PreparacionesController, '/preparaciones',
                 '/preparaciones/<int:id>')


@app.route("/")
def inicio():
    return 'hola amiguitos'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
