# import modelos
from models.receta import RecetaModel
from models.ingrediente import IngredienteModel
from models.preparacion import PreparacionModel
from models.receta_ingrediente import RecetaIngredienteModel
from models.log import LogModel


# import controllers
from controllers.ingrediente import FiltroIngredientesController, IngredienteController, IngredientesController
from controllers.receta import RecetaController, RecetasController
from controllers.preparacion import PreparacionController
from controllers.receta_ingrediente import RecetaIngredientesController


from flask import Flask
from conexion_db import areaConfigBD,base_de_datos
from dotenv import load_dotenv
from flask_restful import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


#carge todas las variables de entorno y de nuestro .en
load_dotenv()

# config de swagger
#esta variable se usa para indicar en que ruta(endpoint) se encontrara la documentacion
#luego de la config levanta el server y entra a ese enlace de la
# 127.0.0.1:5000/api/docs y te mostrara toda la documentacion que hemos realizado
#en swagger hay que ver unos detalles mas internos y lo que aremos es deployar a la nuve este api con heroku
SWAGGER_URL='/api/docs'

#indica la ubicacion del archivo json de swagger
API_URL='/static/swagger.json'

# los blueprints sirven para registrar en el caso que nosotros tengamos un proyecto interno y quuerramos agregarlo al proyecto principal de flask
swagger_blueprint=get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url=API_URL,
    config={
        'appName':'Reposteria Flask - Documentacion Swagger'
    }
)
#fin de swagger


#area de instancia
app=Flask(__name__)
app.register_blueprint(swagger_blueprint)
#cuando only le pasamos app le decimos a todos los dominion,a todas los metodos y a todos los headers hagan lo que sea con las rutas los controladores etc
#para controlar el acceso a nuestra api es x medio de los cors
#origin una lista de paginas que podran tener acceso a mi API('*') para todos los dominios
# methods puedes consultar mi API x defecto tiene todos los methods habilitados(GET,POST,PATH,PUT,DELETE,OPTIONS,HEAD)
# allow_headers = sirve para indicar que cabezeras se pueden enviar x defecto todos
CORS(app=app,origins='*',methods=['GET','POST','PUT','DELETE'],allow_headers='Content-Type') 
api=Api(app)

#area de configuracion
areaConfigBD(app)
base_de_datos.init_app(app)
base_de_datos.create_all(app=app)
# base_de_datos.drop_all(app=app)


#zona de enrutamiento
# api.add_resource(nombrecontrolador,'enpoint')
api.add_resource(IngredientesController,'/ingredientes')
api.add_resource(IngredienteController,'/ingrediente/<int:id>')
api.add_resource(FiltroIngredientesController,'/buscar_ingrediente')

api.add_resource(RecetasController,'/recetas')
api.add_resource(RecetaController,'/receta/<int:id>')

api.add_resource(PreparacionController,'/preparacion','/preparacion/<int:id>')

api.add_resource(RecetaIngredientesController,'/recetas_ingredientes')

@app.route("/")
def inicio():
    return "hola inicio"

if __name__ == "__main__":
    app.run(debug=True,port=5000)