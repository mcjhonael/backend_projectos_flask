from flask_restful import Resource, reqparse
from conexion_db import base_de_datos
from sqlalchemy.exc import IntegrityError
# import models
from models.preparacion import PreparacionModel

class PreparacionController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)
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
        location='json',
        required=True, 
        help='Falta una descripcion'
    )
    serializador.add_argument(
        'receta_id',
        type=int,
        required=True,
        location='json',
        help='Falta receta_id'
    )
    # vamos a mostrar una preparacion
    def get(self,id):

        preparacion=base_de_datos.session.query(PreparacionModel).filter(PreparacionModel.preparacionId==id).first()
        # print(preparacion)
        # print(preparacion.preparacionRecetas.__dict__)
        if preparacion is None:
            return{
                "content":None,
                "message":"Preparacion no existe"
            }
        preparacionDict={
            "id":preparacion.preparacionId,
            "orden":preparacion.preparacionOrden,
            "descripcion":preparacion.preparacionDescripcion,
            "receta_id":preparacion.receta,
        }
        return {
            "content":preparacionDict,
            "message":None
        },200

    # crear una preparacion
    def post(self):
        data=self.serializador.parse_args()

        preparacion=PreparacionModel(preparacionOrden=data.get('orden'),preparacionDescripcion=data.get('descripcion'),receta=data.get('receta_id'))

        try:
            base_de_datos.session.add(preparacion)
            base_de_datos.session.commit()

            json={
                "id":preparacion.preparacionId,
                "orden":preparacion.preparacionOrden,
                "descripcion":preparacion.preparacionDescripcion,
                "receta_id":preparacion.receta
            }
            print(preparacion.__dict__)
            return {
                "content":json,
                "message":None
            },201
        except IntegrityError as err:
            return {
                "content":None,
                "message":"Receta no existe"
            }
        pass
