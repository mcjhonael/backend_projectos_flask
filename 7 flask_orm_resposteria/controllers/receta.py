from flask_restful import Resource,reqparse
from conexion_db import base_de_datos
from models.receta import RecetaModel
from math import ceil

class RecetasController(Resource):
  serializador=reqparse.RequestParser()
  
  #mostrar todas las recetas es casi igual con mostrar y paginarlas
  # def get(self):
  #   resultado=base_de_datos.session.query(RecetaModel).all()
  #   recetas=[]
  #   for receta in resultado:
  #     receta_dicc=receta.__dict__.copy()
  #     del receta_dicc['_sa_instance_state']
  #     recetas.append({
  #       "recetaId":receta_dicc['recetaId'],
  #       "recetaNombre":receta_dicc['recetaNombre'],
  #       "recetaPorcion":receta_dicc['recetaPorcion'].value,
  #     })
  #     print(receta_dicc)
  #   return{
  #     "content":recetas,
  #     "message":None
  #   }

  #crear un receta
  def post(self):
    self.serializador.add_argument(
      'nombre',
      type=str,
      required=True,
      location='json',
      help='ingrese el nombre de la receta'
    )
    self.serializador.add_argument(
      'porcion',
      type=str,
      required=True,
      location='json',
      help='ingrese la porcion',
      choices=['personal','mediano','familiar']
    )
    try:
      data=self.serializador.parse_args()
      nuevaReceta=RecetaModel(recetaNombre=data['nombre'],recetaPorcion=data['porcion'])
      base_de_datos.session.add(nuevaReceta)
      base_de_datos.session.commit()
      return{
        "content":data,
        "message":"Receta exitosa"
      },201
    except:
      return{
        "message":"Hubo un error al guardar la receta, intentelo mas tarde"
      },500


  #mostrar las recetas y paginarlas
  #en la 1era o 2da vuelta asi se muestra
  # offset salteate 0 nada para empezar despues te salteas las 10 primeras recetas y de alli  sucesivamente sirve mucho para paginarlas
  #limit 10 => 10
  # offet 0 => 10

  def get(self):
    self.serializador.add_argument(
      'page',
      type=int,
      required=True,
      location='args',
      help='falta la pagina'
    )
    self.serializador.add_argument(
      'perPage',
      type=int,
      required=True,
      location='args',
      help='falta por pagina'
    )
    data=self.serializador.parse_args()
    
    # Help paginacion (ayudante de paginacion)
    page=data['page'] #pagina inicial
    perPage=data['perPage'] #numero de pagina
    limit=perPage #numero de paginas  a donde puede llegar
    offset=(page-1)*limit#cantidad de datos que deseamos mostrar no es cierto esto
    #fin de helpe pagination  

    #creacion de datos de paginacion
    # SELECT * FROM RECETAS === TOTAL DE RECETAS QUE HAY
    totalRecetas=base_de_datos.session.query(RecetaModel).count()

    itemsPorPagina= perPage if totalRecetas >= perPage else None

    #ceil retorna la parte entera de una division considerando su decimal
    totalPaginas=ceil(totalRecetas/itemsPorPagina)
    
    if page>1:
      paginaPrevia=page-1 if page <= totalPaginas else None
    else:
      paginaPrevia=None
    if totalPaginas>1:
      paginaSiguiente=page+1 if page < totalPaginas else None
    else:
      paginaSiguiente=None
    #fin de la creacion

    #lista para mostrar toda la paginacion
    recetas=base_de_datos.session.query(RecetaModel).limit(limit).offset(offset).all()
    resultado=[]
    for receta in recetas:
      recetaDict=receta.__dict__.copy()
      del recetaDict['_sa_instance_state']
      recetaDict['recetaPorcion']=recetaDict['recetaPorcion'].value
      resultado.append(recetaDict)
    return {
      "content":resultado,
      "pagination":{
        "total":totalRecetas,
        "perPages":itemsPorPagina,
        "paginaPrevia":paginaPrevia,
        "paginaSiguiente":paginaSiguiente,
        "totalPaginas":totalPaginas
      }
    }


# falta 1 clase super importante cuidado