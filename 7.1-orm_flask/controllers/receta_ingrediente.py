from flask_restful import Resource,reqparse
from conexion_db import base_de_datos

# import models
from models.receta import RecetaModel
from models.ingrediente import IngredienteModel
from models.receta_ingrediente import RecetaIngredienteModel
from models.log import LogModel

#de preferencia cuando hagamos una igualdar de un dicc o lista usemos el metodo .copy() para que haga una copia del contenido mas no de la ubicacion de memoria que normalmente pasa
#luego de tener una copia de esos datos recien podemos hacer las modificaciones que deseamos

class RecetaIngredientesController(Resource):
    #aqui es donde se va empezar a armar todo crearemos una receta con sus ingredientes osea llamo tal receta y esta me mostrara los ingredientes que debe tener

    #ingredientes y recetas tiene sus atributos propios independientes aqui vamos a armalos

    #mandare una lista de ingredientes y estos ingredientes deben existir en la base de datos y no existe error xk no podre crear una receta con ingredientes falsos

    serializador=reqparse.RequestParser(bundle_errors=True)
    
    serializador.add_argument(
        'receta_id',
        type=int,
        location='json',
        required=True,
        help='Falta Receta'
    )
    serializador.add_argument(
        'ingrediente_id',
        type=list,
        location='json',
        required=True,
        help='Falta la lista de ingrediente'
    )
    serializador.add_argument(
        'cantidad',
        type=str,
        required=True,
        location='json',
        help='Falta la cantidad'
    )
    def post(self):
        data=self.serializador.parse_args()
        ingredientes=data['ingrediente_id']
        print(data)
        #verificacion x cada parametro enviado empezamos x receta

        try:
            #verificamos si nos estan enviando la receta correcta si existe o no
            receta=base_de_datos.session.query(RecetaModel).filter(RecetaModel.recetaID==data.get('receta_id')).first()
            
            if receta is None:
                raise Exception('receta no existe')

            #ahora si existe la receta!!! verifiquemos que la lista de ingredientes coincidan con los ingredientes q tenemos en bd
            for ingrediente in ingredientes:
                print(ingrediente)
                
                ingredienteEncontrado=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==ingrediente).first()
                print(ingredienteEncontrado)
                
                if ingredienteEncontrado is None:
                    raise Exception('ingrediente no existe')

                nuevaRecetaIngrediente=RecetaIngredienteModel(receta=data['receta_id'],ingrediente=ingrediente,recetaIngredienteCantidad=data['cantidad'])

                base_de_datos.session.add(nuevaRecetaIngrediente)
            base_de_datos.session.commit()
            return{
                "content":"",
                "message":"Creado exitosamente"
            },201

        except Exception as err:
            base_de_datos.session.rollback()
            nuevoLog=LogModel()
            nuevoLog.logRazon=err.args[0]
            
            base_de_datos.session.add(nuevoLog)
            base_de_datos.session.commit()
            return{
                "message":err.args[0],
                "content":None
            },404

