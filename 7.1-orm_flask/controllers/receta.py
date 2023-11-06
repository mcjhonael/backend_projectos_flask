from os import fsdecode
from flask_restful import Resource, reqparse
from conexion_db import base_de_datos
from sqlalchemy.exc import IntegrityError, DataError
from math import ceil

# import modelos
from models.receta import RecetaModel


# clase que se encarga de crear una nueva receta y de paginar las miles de recetas
class RecetasController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)

    # creacion de una receta
    # cuidado cuando dice valores truncate es que se esta rompiendo la estructura base cuando enviamos un valor diferente al que tenemos

    def post(self):
        self.serializador.add_argument(
            'nombre',
            type=str,
            location='json',
            required=True,
            help='Falta receta'
        )
        self.serializador.add_argument(
            'porcion',
            type=str,
            location='json',
            required=True,
            help='Falta porcion',
            choices=['PERSONAL', 'MEDIANA', 'FAMILIAR']
        )
        receta = self.serializador.parse_args()
        print(receta)
        try:
            nuevaReceta = RecetaModel(
                recetaNombre=receta['nombre'], recetaPorcion=receta['porcion'])
            base_de_datos.session.add(nuevaReceta)
            base_de_datos.session.commit()
            return {
                "content": receta,
                "message": "Receta Creada Exitosamente"
            }, 201
        except IntegrityError as e:
            return {
                "message": "Receta existe"
            }, 500
        except DataError as e:
            print(e)
            return{
                "message": "Receta supera el tamanio de caracteres"
            }, 500
        except Exception as e:
            print(e)
            return{
                "message": "Hubo un error al guardar la receta"
            }

    # paginacion de la recetas
    # para esto debemos tener por los args de la url la pagina en la que estamos y hasta que pagina se puede avanzar(page, perPage) para ello creamos nuevos serializadores
    def get(self):
        self.serializador.add_argument(
            'page',
            type=int,
            location='args',
            required=True,
            help='Falta la Pagina'
        )
        self.serializador.add_argument(
            'perPage',
            type=int,
            location='args',
            required=True,
            help='Falta la pagina'
        )

        data = self.serializador.parse_args()
        ########################################
        #waoooooooooo magia pura desde receta accediendo a las preparaciones eso va abajo
        # receta=base_de_datos.session.query(RecetaModel).filter(RecetaModel.recetaID==1).first()

        #con esto ingresamos desde receta a preparaciones
        # for preparacion in receta.preparaciones:
        #     print(preparacion)
            
        # ahora lo aremos desde recetas a recetas_ingredientes
        # print(receta.recetas_ingredientes[0].recetaIngredienteIngredientes)
        # receta.recetas_ingredientes[0].recetaIngredienteIngredientes

        # iteramos
        # for receta_ingrediente in receta.recetas_ingredientes:
        #     print(receta_ingrediente.recetaIngredienteId)
        ########################################

        page = data['page']  # pagina incial o paginaCualquiera
        perPage = data['perPage']  # cuantos recetas mostrar x pagina

        limit = perPage
        offset = (page-1)*limit  # cantidad de datos a mostrar x pagina

        # va contar la cantidad de paginas que tenemos en total
        totalRecetas = base_de_datos.session.query(RecetaModel).count()
        # print(totalRecetas)
        itemsPorPagina = perPage if totalRecetas >= perPage else None

        totalPaginas = ceil(totalRecetas/itemsPorPagina)
        print(totalPaginas)
        if page > 1:
            paginaPrevia = page-1 if page <= totalPaginas else None
        else:
            paginaPrevia = None

        if totalPaginas > 1:
            paginaSiguiente = page+1 if page < totalPaginas else None
        else:
            paginaSiguiente = None
        recetas = base_de_datos.session.query(
            RecetaModel).limit(limit).offset(offset).all()

        resultados = []
        # print(recetas)
        for receta in recetas:
            resultados.append({
                "id":receta.recetaID,
                "nombre":receta.recetaNombre,
                "porcion":receta.recetaPorcion.value,
            })
        # for receta in recetas:
        #     recetaDict=receta.__dict__.copy()
        #     del recetaDict['_sa_instance_state']
        #     recetaDict['recetaPorcion']=recetaDict['recetaPorcion'].value
        #     resultados.append(recetaDict)
        return {
            "content":resultados,
            "paginacion":{
                "totalRecetas":totalRecetas,
                "perPage":itemsPorPagina,
                "paginaPrevia":paginaPrevia,
                "paginaSiguiente":paginaSiguiente,
                "totalPaginas":totalPaginas
            }
        },200


#en este controlador navegamos entre tablas gracias al relationship y sin usar el join una cosa de locos
class RecetaController(Resource):

    def get(self, id):
        receta = base_de_datos.session.query(RecetaModel).filter(
            RecetaModel.recetaID == id).first()

        if receta is None:
            return {
                "message": "Receta no existe",
                "content": None
            }, 404

        diccionario_receta = receta.__dict__.copy()
        del diccionario_receta['_sa_instance_state']
        diccionario_receta['recetaPorcion'] = receta.recetaPorcion.value

        # print(receta.recetas_ingredientes[0].recetaIngredienteIngredientes)

        diccionario_receta['preparaciones'] = []

        for preparacion in receta.preparaciones:
            diccionario_preparacion = preparacion.__dict__.copy()
            del diccionario_preparacion['_sa_instance_state']
            diccionario_receta['preparaciones'].append(diccionario_preparacion)
            # print(preparacion.__dict__)

        diccionario_receta['ingredientes'] = []

        for receta_ingrediente in receta.recetas_ingredientes:
            diccionario_receta_ingrediente = receta_ingrediente.__dict__.copy()
            del diccionario_receta_ingrediente['_sa_instance_state']

            diccionario_receta_ingrediente['ingrediente'] = receta_ingrediente.recetaIngredienteIngredientes.__dict__.copy(
            )

            del diccionario_receta_ingrediente['ingrediente']['_sa_instance_state']
            # print(receta_ingrediente.recetaIngredienteIngredientes)
            print(diccionario_receta_ingrediente)

            diccionario_receta['ingredientes'].append(
                diccionario_receta_ingrediente)

        return {
            "message": None,
            "content": diccionario_receta
        }