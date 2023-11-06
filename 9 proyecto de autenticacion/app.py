# en este proyeto aremos un ADMINISTRADOR DE TAREAS(TASK MANAGER)
# autenticacion
# autorizacion
# olvide password
# enviar correos


from flask import Flask, current_app, render_template, request, send_file
from config.conexion_db import base_de_datos, areaConfigDB
from config.jwt_config import JWTSecret
from dotenv import load_dotenv
from flask_restful import Api
from config.seguridad import autenticador, identificador
from flask_jwt import JWT
from config.configuracion_jwt import manejo_error_JWT
from datetime import datetime
from cryptography.fernet import Fernet
from os import environ, path, remove
from json import loads
from utils.patrones import PATRON_PASSWORD
from re import search
from bcrypt import hashpw, gensalt
from uuid import uuid4
# config sirve para configurar mi SDK cloudinary
from cloudinary import config
#gestiona la carga y la descargar de nuestro archivos
from cloudinary.uploader import upload,destroy


# import models
from models.tarea import TareaModel
from models.usuario import UsuarioModel

# import controllers
from controllers.Usuario import RegistroController, ResetearPasswordController, UsuarioController
from controllers.Tarea import TareasController

load_dotenv()

# area de instancia
app = Flask(__name__)
api = Api(app)

#area de configuracion de nuestro CLOUDINARY
config(
    cloud_name=environ.get("CLOUD_NAME"),
    api_key=environ.get("API_KEY"),
    api_secret=environ.get("API_SECRET")
)


# area de config de SQLALCHEMY
areaConfigDB(app)

# config de secret key
JWTSecret(app)
# cuando inicializamos la clase JWT automaticamente crea una ruta llamada
# /auth con metodo post el cual va recibir las credenciales username y password que ya hemos importado en el metodo autenticador
# & cuando las credenciales coincidan con las de la bd entonces lo que retornara sera una access_token y cuando no coincidan entonces retornara un dict con la description del error, el error y el estado del error
# {
#     "description": "Invalid credentials",
#     "error": "Bad Request",
#     "status_code": 401
# }
# luego entramos a esta pagina https://jwt.io/ y colocamos nuestra token para ver que contiene dentro y como se genero la token
jsonwebtoken = JWT(app=app, authentication_handler=autenticador,
                   identity_handler=identificador)

# para manejar los error de JWT
# 1er metodo de modificacon con el callback es para indicar o igualar a funciones xk recuerda que no podemos usar ()=>{} xk es python
jsonwebtoken.jwt_error_callback = manejo_error_JWT


base_de_datos.init_app(app)
base_de_datos.create_all(app=app)
# base_de_datos.drop_all(app=app)


# en este espacio vamos a modificar nuestro payload
# 2do metodo atravez del decorador y del handle
# este metodo va saltar cuando llamemos a la token osea cuando nos autentiquemos
# todo menos esto que estamos haciendo normal funciona pero ya estamos saltando la vaya metiendonos mas en a libreria flask_jwt al modificar el payload
# recuerda que el payload es el que se le da al frontend para su uso x lo cual vamos a modificarlo para darselo bien mascadito y asi pueda hacer ese cronometro bien vacano
# esta funcion va saltar apenas creas la token ojo
@jsonwebtoken.jwt_payload_handler
def definir_payload(identity):
    # https://www.calculo-sa.es/que-es-jwt/#:~:text=JSON%20Web%20Tokens%20(JWTs)%20son,plano%20en%20formato%20clave%2Dvalor.
    # para saber mas de la inf de las token

    # cuando nos autentiquemos el metodo autenticacion retornar la instancia con la clase con los parametros id y username lo que esto nos devolvera en este atributo identity sera la insatancia de la clase creada en autenticacion osea me mandara el usuario id y username de esa misma persona que ingreso hacer su autenticacion y genero el token
    # print(identity)
    # estos 3 parametros que estamos enviando si o si deben enviarse xk sin falta 1 no se podra crear la token y mandara error x lo cual siempre deben enviar iat,exp,nbf xk x defecto asi dicen la documentacion aunque tambien podemos modificarlo con el atributo JWT_REQUIRED_CLAIMS=['iat','exp','nbf'] x defecto son esos 3 parametros para recien crear la token

    # current_app.config = contiene las variables de configuracion de la aplicacion actual se usa para evitar el error de importacion circular cuando deseamos usar app pero en otros archivos donde hemos realizado importaciones en app.py

    # RETORNA EL TIEMPO QUE DURA LA TOKEN
    print(current_app.config['JWT_EXPIRATION_DELTA'])

    # fecha de creacion de mi token
    creation = datetime.utcnow()

    # fecha de expiracion de mi token seria la fecha de creacion sumado con el tiempo de vida que le dimos la cual nos dara la fecha de expiracion
    expiration = creation + current_app.config['JWT_EXPIRATION_DELTA']

    # EL JWT_NOT_BEFORE_DELTA x defecto tiene una fecha de creacion de 0s entonces practicamente el not_before_delta se va crear con la misma fecha de creacion practicamente
    not_before_delta = creation + current_app.config['JWT_NOT_BEFORE_DELTA']

    user = {
        "id": identity.id,
        "correo": identity.username
    }
    return{
        "iat": creation,
        "exp": expiration,
        "nbf": not_before_delta,
        "usuario": user
    }

# aqui estamos creando rutas fuera de los servicios para poder mostrar html son cosas diferentes ojoo osea en esta ruta /change-password cuando la llamemos lo vamos a usar


@app.route('/prueba-jinja', methods=["GET"])
def prueba_jinja():
    productos = ['pollo', 'manzana', 'platanos', 'cebolla', 'tomate']
    personas = [
        {"nombre": "Eduardo", "sexo": "masculino"},
        {"nombre": "Maria", "sexo": "femenina"},
        {"nombre": "Teresa", "sexo": "femenina"},
        {"nombre": "Titolas", "sexo": "masculino"},
        {"nombre": "Efrain", "sexo": "masculino"},
    ]
    return render_template('prueba-password.jinja', nombre='jhonael', productos=productos, personas=personas)

# para renderizar alguna plantilla solamente lo podemos hacer x el metodo post


@app.route('/change-password', methods=["GET", "POST"])
def cambiar_password():
    if request.method == "GET":
        # imprime la token con su valor como lo estamos enviando
        # print(request.args)

        # sacamos la token de los query params
        token = request.args.get('token')

        # creamos la instancia de la clase Fernet
        fernet = Fernet(environ.get('FERNET_SECRET'))

        try:
            # desencrytamos la token en el cual habia fecha de caducidad y correo
            # retorna un string x lo cual debemos convertirlo
            resultado = fernet.decrypt(bytes(token, 'utf-8')).decode('utf-8')
            # print(resultado)

            # en pocas palabras nos retorna un string x lo cual debemos cambiar a json
            # ? loads permite convertir un formato string a un formato json o diccionario
            resultado = loads(resultado)
            # si la token que nos manda no es la correcta entonces mandara un error del tipo fernet.InvalidToken osa un raise
            # si la token manda un error entonces lo capturamos y lo metemos en un except pero para ello le diremos que cuando ocurra un error que me muestre un html con el error
            print(resultado)

            # vamos a convertir esa fecha que esta en string a una fecha normal Date strptime()
            # cuando queremos de una fecha a un string usamos strftime()
            # como parametro recibe la fecha en string y como 2do parametro como esta estructurado esa fecha con k orden
            fecha_caducidad = datetime.strptime(resultado.get(
                'fecha_caducidad'), '%Y-%m-%d %H:%M:%S.%f')

            # 2022-06-03 21:13:36.014070 nos imprime esto pero alparecer hay fechas distintas con horas diferentes entonces lo que podemos hacer es comparar utcnow vs utcnow tanto de app.py como Usuario.py
            print(fecha_caducidad)

            fecha_actual = datetime.utcnow()
            if fecha_actual < fecha_caducidad:
                print('todabia hay time')
                return render_template('change_password.jinja', correo=resultado.get('correo'))
            else:
                print('ya no hay tiempo')
                return render_template('bad_token.jinja')

        except:
            return render_template('bad_token.jinja')
    elif request.method == "POST":
        data = request.get_json()
        print(data)

        # buscamos al usuario por su correo y le actualizamos la password
        email = request.get_json().get('email')
        password = request.get_json().get('password')

        usuario = base_de_datos.session.query(UsuarioModel).filter(
            UsuarioModel.usuarioCorreo == email).first()

        if not usuario:
            return{
                "message": "Usuario no existe"
            }, 400

        # validamos el formato del password
        if search(PATRON_PASSWORD, password) is None:
            return{
                "message": "Contrasenia muy debil, debe tener al menos 1 mayus, 1 minus, 1 numero, 1 carac. especial y no menos de 6 caracteres"
            }

        # entonces todo bien hasta el momento con usuario y la clave entonces debemos encryptarlo de una vez
        password_bytes = bytes(password, 'utf-8')
        nuevaPwd = hashpw(password_bytes, gensalt()).decode('uft-8')

        # realizamos la actualizacion en la bd
        # le hemos puesto code_status 400 xk cuando mandar el error entonces muestra ese codigo
        try:
            base_de_datos.session.query(UsuarioModel).filter(UsuarioModel.usuarioId == usuario.usuarioId).update({
                "usuarioPassword": nuevaPwd
            })
            base_de_datos.session.commit()
            return{
                "message": "Se realizo el cambio de la password exitosamente"
            }
        except Exception as e:
            print(e)
            return{
                "message": "Hubo un error al actualizar el usuario"
            }, 400


# este es una ruta que tiene por accion subir cualquier tipo de archivo en general pdf, wordk, pptt, img, video, etc CUALQUIER TIPO DE ARCHIVOS
# en el postman como hacemos para mandar cualquier tipo de archivo del front al backend en postman se sigue mandando desde el body pero en otro type ya no  raw si no form-data y creamos 2 llaves (imagen y nombre) y si colocamos el cursor alli nos mostrar k tipo de valor puede tomar TEXT o FILES y escogemos FILEs y cargamos el archivo k deseamos
# *controlador que se encarga de guardar los archivos
@app.route("/subir-archivo-servidor", methods=["POST"])
def subir_archivo_servidor():
    # brinda toda la inforamcion que esta mandando el usuario pero en un formato puro (la imagen en format Hexadecimal y el nombre)
    # print(request.get_data())

    # muestra un dupla inmutable de modificar con una llave llamada imagen
    # ImmutableMultiDict([('imagen', <FileStorage: 'bd_reposteria.png' ('image/png')>)])

    # accedemos a esa llave y obtenemos la instancia de la clase FileStorage
    archivo = request.files.get('imagen')

    # si no me mandan con esa llave el front entonces me mandara error
    if archivo is None:
        return{
            "content": "Archivo no encontrado"
        }, 404

    # filename=> retorna el nombre del archivo
    print(archivo.filename)

    # mimetype => muestra el tipo del archivo que este contiene image/jpeg con esto podemos decir que tipo de archivo estan permitidos nad mas y no metan archivos imnecesarios
    print(archivo.mimetype)

    # debemos casar el nombre del archivo xk aveces es necesario colocar 1 img y la 2da se repite tiene k tener un codigo y si la 3era se repite igual un codigo asi es como se diferencian entre imagenes de iguales
    # lo que pasa es que cuando un usuario intenta colocar una imagen con el mismo nombre de que otro usuario este lo sobreescribe y no se coloca 2 veces entonces de 2 user solo se obtiene 1 img x lo cual esta mal y lo normalmente es que modifiquemos eso
    nombre_inicial = archivo.filename

    # se encarga de separar un string bajo un patron que indique como lo va separar y lo convertira en una lista de string
    # y obtenemos el ultimo valor k seria el formato
    extension = nombre_inicial.rsplit('.')[-1]

    # para crear el nuevo nombre del archivo repetido
    print(type(uuid4()))
    # es te pido uuid pero lo vamos a convertir a type string
    nuevo_nombre = str(uuid4())+'.'+extension

    # recuerda que nuestro servidor es el que estamos usamos en este proyecto entonces el .save(se guarda en el servidor) nos dice en k lugar queremos guardar nuestros archivos
    # estos archivos se guardan en una carpeta media|multimedia|files|img
    # aqui le decimos que se guardara en la carpeta media con la ruta del archivo
    # path.join() le decimos uneme la carpeta media con su archivo archivo.filename
    archivo.save(path.join('media', nuevo_nombre))

    return {
        "message": "archivo subido exitosamente",
        "content": {
            "nombre": nuevo_nombre
        }
    }, 201


# &controlador que se encarge de consultar los archivos
# ^recibe como parametro el nombre del archivo con su extension x la url y retorna la img k busca o el error si no se encontro
@app.route("/multimedia/<string:nombre>", methods=["GET"])
def devolver_imagen_servidor(nombre):
    try:
        # aqui le decimos que el path jale toda la ubicacion de mi proyecto luego unirlo con media y unir tbm con el nombre del archivo y eso me retorna el archivo
        # send_file = retorna el archivo que estamos buscando
        # esto es lo que retorna para el front la imagen k busca o el error en forma de imagen
        return send_file(path.join('media', nombre))
    except:
        # si no encuentra el archivo entonces retorna un archivo not found
        return send_file(path.join('media', 'not_found.jfif'))

# este metodo se encargara de eliminar el archivo del servidor esto va ocurrir cuando el usuario elimine la tarea o si no cuando no termine de llenar el formulario de tarea
@app.route("/eliminar-archivo-servidor/<string:nombre>", methods=['DELETE'])
def eliminar_imagen_servidor(nombre):
    try:
        remove(path.join('media', nombre))
    finally:
        # funciona si el try fue exitoso o si no lo fue, osea, siempre se va a ejecutar
        # si se elimino o no igal dame ese mensaje
        return {
            "message": 'ok'
        }, 204

    #! TODO LO QUE HEMOS VISTO DE SUBIR ARCHIVOS AL SERVIDOR LOCAL DE NUESTRO PROYECTO PERO TIENE UN PROBLEMA XK CUANDO SUBAMOS A UN SERVIDOR ESTE NOS VA A COBRAR POR ALMACENAMIENTO Y AQUI EL 99% SON DE ARCHIVOS MEDIA Y 1% DE NUESTRO PROYECTO (si tenemos un servidor que no nos mida por tamanio de archivo media entonces vacan podremos subirlo pero si no es asi tendremos problemas x el espacio)

# & PARA ESTA SOLUCION VAMOS A SUBIR NUESTRO ARCHIVOS A UN SERVIDOR EN LA NUBLE QUE ES https://cloudinary.com/ RECUERDA 1RO LOGEARTE al parecer funciona este servidor para fotos y videos tambien lo que nos brinda este cloud es que podamos modificar nuestra img como si estuvieramos en el front en cambiar de posicion de color etc

# & 1ro debemos configurar nuestro SDK para poder subir, eliminar imagenes tambien debmos instalar el cloudnary/ ahora entramos al dashboard para ver mas las credenciales y lo configuramos mas arriba y ya no queda nada mas por hacer que crear los endpoint

#?si queremos subir un video debemos colocar el tipo de recurso resource_type="video"
@app.route("/subir-imagen-cloudinary",methods=["POST"])
def subir_imagen_cloudinary():
    imagen=request.files.get('imagen')
    print(imagen)

    #este metodo permite cargar el archivo y subirlo a mi cloudinary
    #lo que nos retorna son muchos datos que nos permite sabes los detaller de la subida en especial secure_url es que guarda el enlace de la subida del archivo o sea ya esta en la nube en la pagina de cloudinary hay una parte que dice (MEDIA LIBRARY) alli se guardan todas las img subidas
    #otra ventaja es que ya no necesitamos cambiar el nombre cuando una imagen se repite de nuevo
    resultado=upload(imagen)
    #lo que queremos retornar es el id_publico osea el nombre del archivo que hemos subido
    return {
        "message":"Archivo subida exitosamente",
        "content":resultado.get('public_id')
    }

@app.route("/eliminar-imagen-cloudinary/<string:id>",methods=["DELETE"])
def eliminar_imagen_cloudinary(id):
    respuesta=destroy(id)
    return {
        "content":respuesta,
        "message":"Imagen Eliminada EXitosamente"
    }

# area de enrutamiento (RUTAS)
api.add_resource(RegistroController, '/registro')

# vamos a ocultar este /login xk ya no sirve xk la autenticacion tiene todo su estructura propia
# api.add_resource(LoginController,'/login')
api.add_resource(UsuarioController, '/usuario')
api.add_resource(TareasController, '/tareas')
api.add_resource(ResetearPasswordController, '/reset-password')


@app.route("/")
def inicio():
    return "amigues"


if __name__ == '__main__':
    app.run(debug=True, port=5000)


# * ojo mientras mas request haga el front al back mas lento le vuelve la aplicacion
# * para eso debemos aprovechar los request para mandar la mayor informacion que se pueda al backend eso tambien la mayor inf y la mejor a la vez
# &tambien la informacion tiene un peso x eso debemos mandar la mejor informacion la precisa
# ^usamos el metodo patch cuando sean muchos campos a modificar y cuando sean unos 2 o 3 entonces el metodo put
#! ya no se utiliza mucho el prefijo JWT si no el BEARER en este caso cambiamos el JWT x BEARER y normal funciona hacerlo x los headers de postman o tambien lo hacemos como esta actualmente

# la carpeta templates permite renderizar codigo html,css,js junto con su metodo render_template() de Flask

# * para anadir comportamiento se refiere meterle js en la carpeta static

# las imagenes nunca se guardan en la base de datos xk seria mucho peso el tipo de datos Blob no lo usamos para guardar en la bd si no que utilizamos el tipo de dato Text que sirve para guardar la ruta en donde se encuentre la imagen la cual no va apuntar a mi misma bd si no a otro servidor de imagenes
# cuando add un nuevo campo en la bd lo que tenemos que hacer es resetear la bd caballero nomas

# & si se puede hacer que cuando enviemos el formulario tengamos que mandar la imagen tambien pero no es recomendable hacerlo asi mandar la tarea con todos sus datos y su imagen de la tarea y no se suele hacer asi xk suele ser mu engorrosa la informacion suele ser un poco confusa la informacion x el lado del backend xk hay que separar el archivo de la imagen en otra carpeta y tambien los datos del formulario
# ? x eso es recomendable hacerlo x rutas exclusiva para la imagen y otra ruta para la creacion de la tarea ojo que tambien podemos hacerlo en el controlador de api rest pero para este ejemplo lo aremos con el decorador @app

#import os
# El módulo OS en Python proporciona funciones para interactuar con el sistema operativo. OS viene bajo los módulos de utilidad estándar de Python. Este módulo proporciona una forma portátil de usar la funcionalidad dependiente del sistema operativo. El módulo os.path es un submódulo del módulo OS en Python que se utiliza para la manipulación de nombres de rutas comunes.
# El método os.path.join() en Python une uno o más componentes de ruta de manera inteligente. Este método concatena varios componentes de ruta con exactamente un separador de directorio ('/') después de cada parte no vacía excepto el último componente de ruta. Si el último componente de ruta que se va a unir está vacío, se coloca un separador de directorio ('/') al final.
# Si un componente de ruta representa una ruta absoluta, todos los componentes anteriores unidos se descartan y la unión continúa desde el componente de ruta absoluta.

# un buena libreria de react https://react-dropzone.js.org/#section-basic-example para poder cargar archivos

# ?como se hace el proceso de subir imagenes el front lo hace en 2 tiempos
# ? 1.- cuando seleccionamos la imagen a subir realmente ya se empieza a subir al servidor y lo k retorna es el nombre de la imagen
# ? 2.- k cuando llenamos el formulario con todos los campos la imagen ya se abra subido y lo k retorna son los campos con Tarea Creada Exitosamente
# ? 3.- ahora si el usuario desea eliminar la tarea entonces la imagen como ya esta cargada en el servidor debemos elimanar

#super informacion para los archivos Profile, runtime, uwsgi 
# https://argentinaenpython.com/django-girls/extensiones-tutorial/heroku/