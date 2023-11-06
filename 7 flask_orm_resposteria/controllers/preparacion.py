from conexion_db import base_de_datos
from flask_restful import Resource, reqparse
from models.preparacion import PreparacionModel

class PreparacionesController(Resource):
  serializador=reqparse.RequestParser(bundle_errors=True)
  serializador.add_argument(
    'orden',
    type=int,
    required=True,
    location='json',
    help='Falta el orden'
  )
  serializador.add_argument(
    'descripcion',
    type=str,
    required=True,
    location='json',
    help='Falta la descripcion'
  )
  serializador.add_argument(
    'receta_id',
    type=int,
    required=True,
    location='json',
    help='Falta receta_id'
  )

  #mostrar una preparacion espeficica
  def get(self,id):
    try:
      preparacion=base_de_datos.session.query(PreparacionModel).filter(PreparacionModel.preparacionId==id).first()
      if preparacion is None:
        raise Exception('Preparacion no existe')
      preparacionDict=preparacion.__dict__.copy()
      del preparacionDict['_sa_instance_state']
      return{
        "message":None,
        "content":preparacionDict
      }

    except Exception as err:
      return{
        "content":None,
        "message":err.args[0]
      }

  #crear una preparacion
  def post(self):
    data=self.serializador.parse_args()

    nuevaPreparacion=PreparacionModel(preparacionOrden=data.get('orden'),preparacionDescripcion=data.get('descripcion'),receta=data.get('receta_id'))
    
    base_de_datos.session.add(nuevaPreparacion)
    base_de_datos.session.commit()

    #ahora podremos retornar los valores ingresador asi
    nuevaPreparacionDicc={
      "preparacionId":nuevaPreparacion.preparacionId,
      "preparacionOrden":nuevaPreparacion.preparacionOrden,
      "preparacion":nuevaPreparacion.preparacionDescripcion,
      "receta_id":nuevaPreparacion.receta
    }
    return{
      "content":nuevaPreparacionDicc,
      "message":"Preparacion creada exitosamente"
    },201