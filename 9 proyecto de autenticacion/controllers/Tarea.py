from flask import current_app
from config.conexion_db import base_de_datos
from flask_restful import reqparse,Resource
from flask_jwt import jwt_required,current_identity
from cloudinary import CloudinaryImage

#import models
from models.tarea import TareaModel


class TareasController(Resource):
    serializador=reqparse.RequestParser(bundle_errors=True)
    serializador.add_argument(
        'titulo',
        location='json',
        required=True,
        help='Falta el titulo',
        type=str
    )
    serializador.add_argument(
        'descripcion',
        location='json',
        required=True,
        help='Falta la descripcion',
        type=str
    )
    serializador.add_argument(
        'tags',
        type=list,
        required=True,
        help='Falta los tags',
        location='json'
    )
    serializador.add_argument(
        'estado',
        choices=['POR_HACER', 'HACIENDO', 'FINALIZADO'],
        type=str,
        help='Falta el estado',
        required=True,
        location='json'
    )
    serializador.add_argument(
        'imagen',
        type=str,
        required=False,
        location='json'
    )
    
    #este metodo post se va encargar de crear las tareas pero recuerda que solamente pueden crear tareas los usuarios que se hagan autenticado para eso usamos el decorador @jwt_required()

    @jwt_required()
    def post(self):
        data=self.serializador.parse_args()
        try: 
            nuevaTarea=TareaModel()
            nuevaTarea.tareaTitulo=data.get('titulo')
            nuevaTarea.tareaDescripcion=data.get('descripcion')
            nuevaTarea.tareaEstado=data.get('estado')
            nuevaTarea.tareaTags=data.get('tags')
            nuevaTarea.tareaImagen=data.get('imagen')

            #este atributo es de la clave foranea en el cual le estamos add el id del usuario que esta realizando la tarea
            nuevaTarea.usuario=current_identity.get('usuarioId')

            #ahora guardamos en la bd
            base_de_datos.session.add(nuevaTarea)
            base_de_datos.session.commit()

            # print(current_identity)
            # print(data)
            return {
                "message":"tarea creado exitosamente",
                "content":{
                    "tareaId":nuevaTarea.tareaId,
                    "tareaDescripcion":nuevaTarea.tareaDescripcion,
                    "tareaEstado":nuevaTarea.tareaEstado.value,
                    "tareaTags":nuevaTarea.tareaTags,
                    # "tareaImagen":nuevaTarea.tareaImagen,
                    "tareaTitulo":nuevaTarea.tareaTitulo,
                    "tareaFechaCreacion":str(nuevaTarea.tareaFechaCreacion),
                    "usuario":nuevaTarea.usuario

                }
            },201
        except Exception as e:
            base_de_datos.session.rollback()
            return{
                "message":"Error al crear una tarea",
                "content":e.args
            },400

    #ESTE METODO SE VA ENCARGAR DE DEVOLVER TODAS LAS TAREAS QUE TIENE UN USUARIO
    @jwt_required()
    def get(self):
        #current me devuelve todos los atributos de la persona que hizo el token con los mismo nombres de su atributo de las columnas
        print(current_identity.get('usuarioId'))

        tareasEncontradas=base_de_datos.session.query(TareaModel).filter(TareaModel.usuario==current_identity.get('usuarioId')).all()
        
        resultado=[]
        for tarea in tareasEncontradas:
            
            tareaDict=tarea.__dict__.copy()
            del tareaDict['_sa_instance_state']
            tareaDict['tareaFechaCreacion']=str(tareaDict['tareaFechaCreacion'])
            #retorna una instancia de la clase Enum pero para acceder a su valor utilizamos .value xk este metodo es propio de la clase Enum
            tareaDict['tareaEstado']=tareaDict['tareaEstado'].value

            #esto es una instancia de la clase CloudinaryImage
            # respuestaCD=CloudinaryImage(tarea.tareaImagen)
            #este metodo url permite tener la ruta para acceder al recurso osea el ejemplo  https://res.cloudinary.com/jhonael/image/upload/aju27sbwk8bhnr1zozyz.png
            # print(respuestaCD.url)
            # tareaDict['tareaImagen']=respuestaCD.url


            #?AHORA LE AREMOS UNA MODIFICACIONES A LA IMAGEN DESDE EL BACKEND Y ESTE NOS RETORNA UNA ETIQUETA <img src="image.jpg" /> LISTA PARA QUE EL FRONTEND PUEDA RENDERIZAR EN FORMA DE str YA NO EN https:// y para dar efecto a los videos cambiamos el image x el video y usamos la clase CloudinaryVideo()
            respuestaCD=CloudinaryImage(tarea.tareaImagen).image(border="20px_solid_rgb:000", height=260, crop="scale")
            tareaDict['tareaImagen']=respuestaCD

            #?en esta pagina tenemos todas la cosas que podemos hacer con clodinary dede el backend en modificaciones de imagenes
            # https://cloudinary.com/documentation/transformation_reference


            print(respuestaCD)
            resultado.append(tareaDict)
        # userDict=user.__dict__
        # print(user)
        return{
            "message":"mostrar tareas",
            "content":resultado
        }


#^LO MEJOR DE CLOUDINARY SE ESPECIALIZA EN SUS TRANSFORMACION https://cloudinary.com/console/c-08d6f717489923426c43c172c04fba/transformation_editor?createNewTransformation=true

#? para saber mas de la integracion veamos esta page 
#? https://cloudinary.com/documentation/django_integration