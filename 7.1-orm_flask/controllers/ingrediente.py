from flask_restful import Resource, reqparse
from conexion_db import base_de_datos
from sqlalchemy.exc import IntegrityError, DataError

# import models
from models.ingrediente import IngredienteModel
from models.log import LogModel

# validador de parametro
serializador = reqparse.RequestParser()

# crea el argumento con las caracteristicas adecuadas
serializador.add_argument(
    "nombre",
    type=str,
    required=True,
    location='json',
    help="Falta un nombre",
)

# un crud completo de la tabla ingredientes
#es muy important siempre usar un try except cuando hagamos un insert, update,delete

class IngredientesController(Resource):
    def get(self):
        # .query solamente nos trae la consulta sql entonces .all nos trae todos los registros q ya habiamos hablando que registro=instancia de la clase
        # retorna una lista de instancia de la clase Ingrediente
        # 1 forma de obtener los registros
        # ingredientes=IngredienteModel.query.all()

        # 2da forma de obtener los registros
        ingredientes = base_de_datos.session.query(IngredienteModel).all()

        # hay 2 manejar para mandar al front puede ser por la clase accediendo a sus atributos propios o tambien usando los [] de la nueva instancia
        # solamente es para darle mejor forma ya que va mostrar los nombres de los atributos q hemos colocado en la clase
        resultado = []
        for ingrediente in ingredientes:
            ingredienteDicc = ingrediente.__dict__
            del ingredienteDicc['_sa_instance_state']
            resultado.append({
                "id": ingrediente.ingredienteId,
                "nombre": ingrediente.ingredienteNombre,
            })
        return {
            "content": resultado,
            "message": None
        }, 200

    def post(self):

        # retorna un diccionario del front con el valor enviado
        data = serializador.parse_args()

        try:
            # una vez obtenido el valor del front debemos tener en cuenta que cuando se hace un nuevo registro de ase asi
            # tabla es la clase, la tabla tiene muchos registro o 1 registro a insertar por lo tanto un registro es un objeto de la clase tabla o una instancia => nosotros debemos crear una instancia de la clase agregando los valores asi es la cosa tabla=clase registro=instancia de clase

            # 1ra forma de crear un registro
            # nuevoIngrediente=IngredienteModel()
            # nuevoIngrediente.ingredienteNombre=data['nombre']
            # print(nuevoIngrediente)

            # 2da forma mas rapida de crear un registro
            nuevoIngrediente = IngredienteModel(
                ingredienteNombre=data['nombre'])
            # print(nuevoIngrediente)

            # registro creado entonces debemos agregarlo a nuestra base de datos
            base_de_datos.session.add(nuevoIngrediente)

            # como ya esta agregado a la base de datos para conservar ese cambio debemos darle un commit asi perdurara ese registro en la bd
            # ojo si por razon el frontend no manda el valor correcto entonces al hacer el commit lanzara un error o exception que debemos controlar
            base_de_datos.session.commit()

            # 1ra forma de mandar al frontend una respuesta
            # cuidado cuando creamos un nuevo registro en post parece que no podemos usar el metodo __dict__ x lo cual le pasamos un json
            # para solucionar este problema debemos sacar una copia de ese ingrediente y recien eliminar
            # copia
            # ingredienteDicc=nuevoIngrediente.__dict__

            # recien eliminamos
            # del ingredienteDicc['_sa_instance_state']

            # el unico problema es que mandaremos al front un resultado poco entendible lo que podemos hacer es crear un json y mandarle vacano
            # return {
            #     "content":ingredienteDicc,
            #     "message":"Ingrediente Creado Exitosamente"
            # },201

            # 2da forma de hacerlo es mas sensillo x un json accediendo a la clase y a sus atributos directamente
            json = {
                "id": nuevoIngrediente.ingredienteId,
                "nombre": nuevoIngrediente.ingredienteNombre
            }
            error = None
            return {
                "content": json,
                "message": "Ingrediente Creado Exitosamente"
            }, 201

        # error que podria surgir al ingresar un ingrediente en la
        # 1 que el nombre del ingrediente sea demasiado largo de lo normal
        # 2 que intenten colocar un ingrediente repetido xk no pasa eso
        # 3 entre otras cosas
        # para esto entonces debemos manejar las exceptiones y controlarlar para luego guardarla en una tabla logs
        except IntegrityError as err:
            error = err
            return{
                "message": "ingrediente duplicado"
            }, 500
        except DataError as err:
            error = err
            return {
                "message": "error al ingresar el ingrediente"
            }, 500
        except Exception as error:
            error = err
            return {
                "message": "Error Desconocido"
            }, 500
        finally:
            if error is not None:
                base_de_datos.session.rollback()
                nuevoLog = LogModel()
                nuevoLog.logRazon = error.args[0]
                base_de_datos.session.add(nuevoLog)
                base_de_datos.session.commit()


class IngredienteController(Resource):
    def get(self, id):
        # si no le pongo .first() me trae la consulta sql pero yo kiero el resultado no la query
        # en una busqueda o lo encuentras o no lo encuentras
        # ingrediente = base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId == id).first()

        # 2da forma mas corta x filter_by()
        ingrediente = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente is None:
            return {
                "content": None,
                "message": "Ingrediente no existe"
            }, 404
        print(ingrediente)
        json = {
            "id": ingrediente.ingredienteId,
            "nombre": ingrediente.ingredienteNombre,
        }
        return {
            "content": json,
            "message": None
        }, 200

    def put(self, id):
        data = serializador.parse_args()
        try:
            # retorna si esta o no ese ingrediente en la busqueda
            ingrediente = base_de_datos.session.query(
                IngredienteModel).filter_by(ingredienteId=id).first()

            if ingrediente is None:
                return {
                    "content": None,
                    "message": "Ingrediente no existe"
                }, 404

            ingrediente.ingredienteNombre = data['nombre']
            base_de_datos.session.commit()
            json = {
                "id": ingrediente.ingredienteId,
                "nombre": ingrediente.ingredienteNombre,
            }
            return {
                "content": json,
                "message": "Ingrediente Actualizado correctamente"
            }, 201
        except DataError as err:
            return {
                "content": None,
                "message": "El ingrediente supera el tamanio de caracteres"
            }
        except Exception as err:
            return {
                "content": None,
                "message": "Ingrediente no se actualizo"
            }

    def delete(self, id):
        # 1ra forma de realizar una eliminar simple
        # parece que no funciona bien descartado abria que revisarlo
        # ingrediente =base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==id).first()
        # if ingrediente is None:
        #     return{
        #         "content":None,
        #         "message":"Ingrediente no existe"

        #     },404

        # base_de_datos.session.delete(ingrediente)
        try:
            base_de_datos.session.query(IngredienteModel).filter(
                IngredienteModel.ingredienteId == id).delete()

            base_de_datos.session.commit()

            return {
                "content": None,
                "message": "Ingrediente Eliminado"
            }, 204
        except:
            return{
                "content": "error al eliminar el ingrediente", 
                "message": None
            }, 500


# un buscador por nombre de ingrediente para ello necesitamos usar un metodo get y parte que no podemos usar este serializador xk lo aremos por el args y no por el body x eso creamos otro serializador

serializadorFiltro = reqparse.RequestParser()
serializadorFiltro.add_argument(
    'nombre',
    type=str,
    location='args',
    required=True,
    help='No se encontro buscador'
)


class FiltroIngredientesController(Resource):
    def get(self):
        filtro = serializadorFiltro.parse_args()

        # retorna una lista de las coincidencias []
        resultados = base_de_datos.session.query(IngredienteModel).filter(
            IngredienteModel.ingredienteNombre.like(f'%{filtro["nombre"]}%')).all()

        # 1ra forma de hacerlo mas corta
        # if len(resultados)==0:
        #     return {
        #         "content":None,
        #         "message":"Ingrediente no existe"
        #     },404
        # resultado_final=[]
        # for ingrediente in resultados:
        #     resultado_final.append({
        #         "id":ingrediente.ingredienteId,
        #         "nombre":ingrediente.ingredienteNombre,
        #     })
        # return {
        #     "content":resultado_final,
        #     "message":"Ingrediente encontrado"
        # },200

        # segunda forma
        # el metodo .with_entities() sirve par retornar la informacion que solamente deseamos mostrar osea atributos que solamente keramos esto es cuando queremos mostrar informacion seleccionada
        # columnas q solamente keremos mostrar

        # retorna una lista de tuplas = a type Row
        # al usar with_entities nos retorna una lista de objetos de la clase Row
        # resultado=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteNombre.like('%{}%'.format(filtro['nombre']))).with_entities(IngredienteModel.ingredienteNombre).all()

        # lo que pasara nos traera los resultado de type row con este metodo y con el otro metodo nos da de class entonces usamos _asdict para convertirlo de type Row a un dicc normal

        # segunda forma de hacerlo
        # for registro in resultado:
        #   print(type(registro))
        #   #lo convierte en un json serializado trabaja para los types Row ._asdict()
        #   print(registro._asdict())
        #   resultado_final.append(registro._asdict())
        # return{
        #   "message":"aqui filtro",
        #   "content":resultado_final
        # }

        # 2da forma de hacerlo
        if len(resultados) == 0:
            return {
                "content": None,
                "message": "Ingrediente no existe"
            }, 404
        resultado_final = []

        for ingrediente in resultados:
            ingredienteDicc = ingrediente.__dict__.copy()
            del ingredienteDicc['_sa_instance_state']
            resultado_final.append({
                "id": ingredienteDicc['ingredienteId'],
                "nombre": ingredienteDicc['ingredienteNombre'],
            })
        return {
            "content": resultado_final,
            "message": None
        }, 200
