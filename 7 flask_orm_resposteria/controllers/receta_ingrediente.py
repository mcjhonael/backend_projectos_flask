from flask_restful import Resource, reqparse
from conexion_db import base_de_datos

#import models
from models.receta import RecetaModel
from models.ingrediente import IngredienteModel
from models.log import LogModel
from models.receta_ingrediente import RecetaIngredienteModel


class RecetaIngredientesController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)
    serializador.add_argument(
        'receta_id',
        type=int,
        required=True,
        location='json',
        help='Falta el id de la receta',
    )
    serializador.add_argument(
        'ingredientes_id',
        type=list,
        required=True,
        location='json',
        help='Falta el id del ingrediente'
    )

    def post(self):
        data = self.serializador.parse_args()

        receta_id = data['receta_id']
        ingredientes_id = data.get('ingredientes_id')
        print(ingredientes_id)
        # cada vez que usemos la base de datos hagamos un try siempre
        try:
            # 1 buscar si existe esa receta
            receta = base_de_datos.session.query(RecetaModel).filter(
                RecetaModel.recetaId == receta_id).first()
            if receta is None:
                raise Exception('Receta no existe')

            # 2 iterar la lista de ingredientes asociado a esa receta ya que ingredientes_id va ser la posicion final del ultimo ingrediente x lo cual hay que mostrarlo hasta alli todo
            for ingrediente in ingredientes_id:

                # buscamos si el ingrediente existe
                # la list de ingredientes que yo mande por el body debe coincider con los mismo ingredientes que tengo en mi tabla ingredientes y si no es asi pues err automaticamente geniall
                ingredienteEncontrado = base_de_datos.session.query(IngredienteModel).filter(
                    IngredienteModel.ingredienteId == ingrediente['ingrediente_id']).first()
                if ingredienteEncontrado is None:
                    raise Exception('Ingrediente incorrecto')
                nueva_receta_ingrediente = RecetaIngredienteModel(
                    ingrediente=ingrediente['ingrediente_id'], receta=receta_id, recetaIngredienteCantidad=ingrediente['cantidad'])
                base_de_datos.session.add(nueva_receta_ingrediente)

            # basta con que no exista un ingrediente y se anula toda la operacion
            base_de_datos.session.commit()
            return{
                "message": "Agrego Exitosamente"
            }, 201
        except Exception as err:
            base_de_datos.session.rollback()
            nuevoLog = LogModel()
            nuevoLog.logRazon = err.args[0]
            base_de_datos.session.add(nuevoLog)
            base_de_datos.session.commit()
            print(err.args)
            print(err)
            return{
                "message": err.args[0],
                "content": None
            }
            
            # si intento ingresar una receta o ingrediente que no existen entonces me mandara un err


# para generar un error aproposito

# try:
#   raise Exception('aqui va el mensaje de error que kiero visualizar')
# except Exception as err:
#   print(err)# aqui consumo el error que he creado con el raizse
