# usamos este controlador de Usuario por que es el usuario el que se registra en la bd
# y xk 1ro debemos registrarnos antes de iniciar session OJO!!

from flask import request
from flask_restful import Resource, reqparse
from config.conexion_db import base_de_datos
from sqlalchemy.exc import IntegrityError
# este modulo se encarga de validar la clave enviada y el patron para k lo que enviemos tenga la misma expresion regular
from re import search
from utils.patrones import PATRON_CORREO, PATRON_PASSWORD
# esta libreria bcrypt nos permite hashear nuestra clave para mayor seguridad
# hashpw = sirve para hashear nuestra clave
from bcrypt import hashpw, gensalt, checkpw
from flask_jwt import jwt_required
# el retorno de identificador que se encuentra dentro de seguridad esa funcion lo que retornara al usuaerio y lo guardara en current_identity asi k ya podemos sacarlo
from flask_jwt import current_identity
from cryptography.fernet import Fernet
from os import environ
from datetime import datetime, timedelta
from json import dumps
from config.enviar_correo import enviarCorreo

# import models
from models.usuario import UsuarioModel


class RegistroController(Resource):

    serializador = reqparse.RequestParser(bundle_errors=True)
    serializador.add_argument(
        'nombre',
        type=str,
        location='json',
        required=True,
        help='Falta el nombre'
    )
    serializador.add_argument(
        'apellido',
        type=str,
        location='json',
        required=True,
        help='Falta el apellido'
    )
    serializador.add_argument(
        'correo',
        type=str,
        location='json',
        required=True,
        help='Falta el correo'
    )
    serializador.add_argument(
        'password',
        type=str,
        location='json',
        required=True,
        help='Falta el password'
    )
    serializador.add_argument(
        'telefono',
        type=str,
        location='json',
        required=True,
        help='Falta el telefono'
    )

    # aqui vamos a registrar los datos del usuario para k luego pueda hacer login
    def post(self):
        data = self.serializador.parse_args()

        # print(data)
        # una vez obteniendo los datos debemos guardarlo en la bd pero antes debemos evaluar que los datos sean los correctos nombre y apellido normal la cosa empieza en correo, password, telefono
        correo = data['correo']
        password = data['password']

        # retorna un match cuando si coincide con ese patron creado y None cuando a fallado
        # print(search(PATRON_CORREO,correo))

        if search(PATRON_CORREO, correo) is None:
            return {
                "message": "Correo Incorrecto"
            }, 400
        if search(PATRON_PASSWORD, password) is None:
            return{
                "message": "Password Incorrecto minimo 6 caracteres una mayuscula,una miniscula y u simbolo especial"
            }
        try:
            nuevoUsuario = UsuarioModel(
                usuarioNombre=data.get('nombre'),
                usuarioApellido=data.get('apellido'),
                usuarioTelefono=data.get('telefono'),
                usuarioCorreo=correo
            )

            # ahora ya hemos validado el correo faltaria la clave entonces la clave tbm esta validada pero lo que debemos hacer ahora es encryptar la clave x mayor seguridad

            # bytes es un tipo de dato que recibe 2 parametros 1 el string a convertir y en que codificacion esta ese string
            passwordBytes = bytes(password, "utf-8")

            print(passwordBytes)
            # gensalt() = permite combiar mi clave con cosas aleatorias para la seguridad de la clave podemos pasarle como parametros cuantas vueltas tiene k dar
            # el gensalt tambien es en bytes
            print('holi')
            print(gensalt(rounds=10))
            salt = gensalt(rounds=10)

            # recibe 2 parametros el password en tipo bytes y un salt() x defecto es el tambien en bytes por ende cuando vamos a hashear tambien nos dara en type bytes x lo cual debemos transformarlo a string
            hashPwd = hashpw(passwordBytes, salt)

            # con decode vamos a decodificar nuestro bytes a un formato string osea utf-8
            hashPwd = hashPwd.decode('utf-8')
            print(hashPwd)

            # una vez decodificado a string entonces vamos a colocar esa clave a campo usuarioPassword y hacer su commit para conservar los cambios
            nuevoUsuario.usuarioPassword = hashPwd
            base_de_datos.session.add(nuevoUsuario)
            base_de_datos.session.commit()

            return {
                "content": None,
                "message": "Usuario Creado Exitosamente"
            }, 201

        except IntegrityError as e:
            base_de_datos.session.rollback()
            return{
                "message": "El correo ya existe",
            }, 500

        except Exception as e:
            base_de_datos.session.rollback()
            return{
                "message": "Error al ingresar el usuario",
                "content": e.args
            }, 500

# para el login debemos recibir por el body el correo y el password


class LoginController(Resource):
    serializador = reqparse.RequestParser(bundle_errors=True)
    serializador.add_argument(
        'correo',
        type=str,
        required=True,
        location='json',
        help='Falta el correo'
    )
    serializador.add_argument(
        'password',
        type=str,
        required=True,
        location='json',
        help='Falta el password'
    )

    def post(self):
        data = self.serializador.parse_args()
        usuario = base_de_datos.session.query(UsuarioModel).filter_by(
            usuarioCorreo=data['correo']).first()

        if usuario is None:
            return{
                "message": "Usuario no encontrado"
            }, 404
        password = bytes(data.get('password'), 'utf-8')
        usuarioPwd = bytes(usuario.usuarioPassword, 'utf-8')

        # este metodo checkpw se encarga de validar la contrasenia no se como lo ara pero si lo hace de una manera sorprendente no me devolvera la contrasenia deshasheada si no k retorna True si la clave coincide y False si la clave no coincide
        resultado = checkpw(password, usuarioPwd)

        # hasta aqui ya coincide el correo y la clave ahora que aremos retornos para decirle si encontro o no el usuario
        if resultado:
            #! cuando obtengemos el resultado lo que aremos es generar la token de acceso para k el usuario pueda cambiar su perfil o lo que sea
            return{
                "content": "usuario encontrado"
            }, 200
        else:
            return{
                "message": "Usuario no encontrado"
            }, 400


# si encontro el usuario desde ese mismo momento ese usuario ya se debe dar un tiempo en que su cuenta este en session para eso usaremos los JSON WEB TOKEN(JWT)


# esto es una token en general es un hash en el cual nos identifica x ejm cuando nosotros generamos una token del banco sigue un patron que esta regitro a nuestra cuenta de la bd del banco
# ejmplo si mando 1924 podriamos decir k el patron que tenemos es 1 y 9 impart y 2 y 4 patron par pero si mandamos 1957 entonces todo cambiaria al coincidir con el patron estamos diciendo que si somos nosotros lo que estamos entrando a la app

# diferencia de una token natural y JWT es lo mismo solamente que esta basado en json osea tiene una estructura json
# jwt tiene una structura de 3 partes
# ? jfkajfkajbfkjabf.janfjanbfjkabfsk.akljnajlkfbakj
# todo: Header la cabecera de mi token aqui se guarda el tipo de la token osea si es una token normal o JWT tambien se guarda el algoritmo de encriptacion osea cuando nosotros enviemos la token  en k algoritmo debe encriptarlo y en k algoritmo debe desencriptarlo . Payload es la parte util de nuestra token aqui se guarda la data {iat:fecha decreacion de la token 2022-06-04 11:40, exp:fecha de expiracion de la token para que la token tenga un tiempo de vida limitado 2022-06-04 12:40 ejm le damos 1 hora de session ojo estas fechas se manejan con la hora del servidor, adicional:id|nombre|correo todo del usuario xk sirve esta este adicional xk el front interactua mas con el Payload x lo cual va poder desencryptarlo y podemos observar esta informacion del json} . signature osea la firma de la token k no se va poder desencrytar y es my segura

# ?el front interactua con el Payload a poder desencrytarlo y verlo pero no va poder modificarlo en caso lo haga generara otra token si el front tiene la firma entonces si podra modificar las fechas


# esta clase se encargara del perfil del usuario
# recuerda que la token debe estar en una ruta protegida
# si nos encargamos del perfil del usuario debe estar en una ruta protegida y xk? xk es info personal k solamente puede verlo el usuario autenticado nadie mas

# en una peticion las token de acceso se mandan x los headers no es recomendable hacerlo x el body
# x la cabecera llamada Authorization se manda las token
class UsuarioController(Resource):
    # * con el decorador nosotros podemos decir que este metodo de la clase tiene k ser protegido
    # ^ con esto estamos diciendo que este metodo debe ser protegido
    # ?codigo 401 para indicarle que la ruta es protegida
    # hast enviar el current_identity ya es la config basica de JWT lo adicional es el resto que aremos darle mas tiempo de session, config los mensajes, etc

    # ? al tener este decorador nos dicen que solamente podemos acceder a este metodo get es con una token que debemos enviar y si no tiene token entonces no podemos acceder a este metodo
    # para este metodo hemos enviado una token x los header Authorization value JWT token....
    @jwt_required()
    def get(self):
        print(current_identity)
        # aqui podemos eliminar el _sa_instance_state o tambien desde su inicio
        del current_identity['_sa_instance_state']
        del current_identity['usuarioPassword']
        return{
            "content": current_identity
        }

    # para poder hacer una actulizacion parcial osea que no necesita actualizar todos los campos si no el que deseo actualizar

    # para este ejemplo enviaremos de otra manera la token para hacerlo de esta manera debemos cambiar la variable de config add otra clave ya no el prefijo JWT si no el BEARD

    # si la token falla nunca podra acceder a este metodo
    @jwt_required()
    def patch(self):
        serializador = reqparse.RequestParser()
        serializador.add_argument(
            'nombre',
            type=str,
            location='json',
            required=False,
        )
        serializador.add_argument(
            'apellido',
            type=str,
            location='json',
            required=False,
        )
        serializador.add_argument(
            'correo',
            type=str,
            location='json',
            required=False,
        )
        serializador.add_argument(
            'password',
            type=str,
            location='json',
            required=False,
        )
        serializador.add_argument(
            'telefono',
            type=str,
            location='json',
            required=False,
        )

        # el current_identity seria el diccionario que nos esta llegando con la informacion del metodo identificador(payload)
        data = serializador.parse_args()

        # print(current_identity.get('usuarioId'))
        usuarioId = current_identity.get('usuarioId')
        usuarioEncontrado = base_de_datos.session.query(
            UsuarioModel).filter(UsuarioModel.usuarioId == usuarioId).first()

        # ya no necesitamos verificar si existe o no el usuario xk al mandar la token es k si o si existe el usuari
        # # hemos encontrado el user entonces lo que debemos hacer es que si nos mandar el password debemos encryptarlo y guardarlo en la base de datos
        # le decimos nuevoPwd=None xk si no tiene clave entonces mandara un error xk buscara esa variable y como no existe ERROR en cambio con el None ya nos evitamos eso
        nuevoPwd = None
        if data.get('password') is not None:
            if search(PATRON_PASSWORD, data.get('password')) is None:
                return{
                    "message": "La contraseña debe tener al menos 1 mayus, 1minus, 1 num y 1 caract"
                }, 400
            print('hay password')
            pwdb = bytes(data.get('password'), 'utf-8')
            salt = gensalt(rounds=10)
            nuevoPwd = hashpw(pwdb, salt).decode('utf-8')
        print(nuevoPwd)

        # en esta parte ya vamos a guardarlo en la base de datos todo listo es magico lo que le mandemos por el body entonces este lo guardara
        try:

            # sin el uso del filter
            # base_de_datos.session.query(UsuarioModel).update({
            # 2 formas de hacerlo con model y con comillas
            # UsuarioModel.usuarioNombre:'lorenzo'
            # "usuarioNombre":"pacola"
            # })

            # con el filter
            usuarioUpdate = base_de_datos.session.query(UsuarioModel).filter(UsuarioModel.usuarioId == usuarioEncontrado.usuarioId).update({

                "usuarioNombre": data.get('nombre') if data.get('nombre') is not None else usuarioEncontrado.usuarioNombre,

                "usuarioApellido": data.get('apellido') if data.get('apellido') is not None else usuarioEncontrado.usuarioApellido,

                "usuarioCorreo": data.get('correo') if data.get('correo') is not None else usuarioEncontrado.usuarioCorreo,

                "usuarioTelefono": data.get('telefono') if data.get('telefono') is not None else usuarioEncontrado.usuarioTelefono,

                "usuarioPassword": nuevoPwd if nuevoPwd is not None else usuarioEncontrado.usuarioPassword
            })
            base_de_datos.session.commit()
            return{
                "message": "Usuario actualizado correctamente"
            }, 201
        except IntegrityError:
            # eso va saltar cuando un usuario intente actualizar su correo por alguno de sus compas entonces el sistema lo revotara
            return{
                "message": "Ya existe un usuario con este correo, no se puede duplicar el correo"
            }, 400

# clase que se encarge de resetear la clave
# ? la finalidad de este srvicio va hacer que cuando deseemos cambiar la clave este nos mandara un mensaje al correo de nuestro login para poder cambiarlo


class ResetearPasswordController(Resource):
    serializador = reqparse.RequestParser()
    serializador.add_argument(
        'correo',
        type=str,
        location='json',
        required=True,
        help='Falta el correo'
    )
    # este metodo no es protedigo x ende no se espera una token ni menos un usuario entonces cuando busquemos al usuario si lo validamos si entonces o no

    def post(self):
        data = self.serializador.parse_args()
        # print(data)
        correo = data.get('correo')

        if search(PATRON_CORREO, correo) is None:
            return{
                "message": "Formato de correo incorrecto"
            }, 400

        usuario = base_de_datos.session.query(
            UsuarioModel).filter_by(usuarioCorreo=correo).first()
        print(usuario)

        # if usuario is None:
        # es lo mismo pero dira si no hay usuario has esto
        if not usuario:
            # te explico lo que puede ocurrir si mandamos este mensaje el usuario al no coincidir con el correo entonces lo que ara es un bombardeo de peticiones tambien llamado ataque de denegacion de servicio o DoS x tema de seguridad y evitar esto le podemos mandar  "SI SE ENVIO EL CORREO CON CAMBIO DE PASSWORD" sea o no el correo igual decirle si no ese gil no va atracar duro pero como andamos aprendiendo entonces colocamos igual nomas
            return{
                "message": "usuario no encontrado"
            }, 404

        # ?para enviar un correo tambien debemos enviar una token por lo cual debemos crear esa token nosotros
        # para ello usaremos la libreria fernet para encrytar y desencrytar

        # https://cryptography.io/en/latest/installation/
        # pip install cryptography

        # &Fernet garantiza que un mensaje cifrado conella no puede ser manipulado ni leído sin laclave. Fernet es una implementación decriptografía autenticada simétrica (tambiénconocida como "clave secreta").

        # con esto creamos nuestra token pero lo guardaremos en los archivo .env
        # key=Fernet.generate_key()
        # print(key)

        # ?una vez creada debemos pasarle a nuestra clase Fenert

        fernet = Fernet(environ.get('FERNET_SECRET'))

        # me muestra una instancia de la clase Fernet
        # print(fernet)

        # ahora vamos a empezar a encryptar
        # mensaje='holi soy el secretito'

        # tenemos que convertirlo a bytes y decodificarlo a string
        # mensaje_encryptado=fernet.encrypt(bytes(mensaje,'utf-8')).decode('utf-8')
        # print(mensaje_encryptado)

        # proceso de desencrytacion
        # mensaje_desencryptado=fernet.decrypt(bytes(mensaje_encryptado,'utf-8'))
        # print(mensaje_desencryptado)

        # ahora vamos a crear un json
        mensaje = {
            # cuanto tiempo va durar mi token creada \ hay que convertirlo a str xk esta en formato fecha
            "fecha_caducidad": str(datetime.utcnow()+timedelta(hours=2)),
            "correo": correo
        }

        # para poder encryptarlo necesitamos convertirlo a str
        # necesitamos convertir este mensaje que esta a json string a json para eso usamos dumps
        mensaje_json = dumps(mensaje)

        # normal puede encryptar json
        mensaje_encryptado = fernet.encrypt(
            bytes(mensaje_json, 'utf-8')).decode('utf-8')

        # una vez encryptado ya podemos enviar correo pero lo aremos en otro archivo para tener mas orden
        print(correo)

        # la mejor manera de enviar ese mensaje encryptado es atravez del queryParams

        # la url nativa osea host + /
        print(request.host_url)

        link = request.host_url+"change-password?token={}".format(
            mensaje_encryptado)

        # entre metodo recibe un correo y el texto en el cual se va en ese correo cuando lo enviemos
        enviarCorreo(correo, '''
                <!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@600&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div
      style="
        display: flex;
        background: #f9f9f9;
        font-family: 'Be Vietnam Pro', sans-serif;
        justify-content: center;
      "
    >
      <div
        style="
          justify-content: center;
          width: 50%;
          flex-direction: column;
          justify-content: flex-end;
          background-color: white;
          padding: 10px 50px;
        "
      >
        <div style="justify-content: center; display: flex">
          <img
            width="138"
            src="https://ci3.googleusercontent.com/proxy/xbGGyYfNO7rOwB3cJ8GvQ_6GUpaWXoqPKpUmrMJDjD2gVRFyUARcwh0qhbWv92i3qb1zJj3c9PYNULP_B3wHWJY--pjeXQiAyt6s5ETJieJ41Gy3loYi3AINdO8gJTk=s0-d-e1-ft#https://cdn.discordapp.com/email_assets/592423b8aedd155170617c9ae736e6e7.png%22/%3E"
          />
        </div>
        <div>
          <div style="margin-top: 70px">
            <div>
              <h2 style="color: #585555; font-weight: 500">Hola, {}</h2>
            </div>
            <div>
              <p style="color: #919191">
                Haz clic en el siguiente botón para restablecer tu contraseña de
                Discord. Si no has solicitado una nueva contraseña, ignora este
                correo.
              </p>
            </div>
            <div style="margin-top: 70px; margin-bottom: 70px">
              <a
                href="{}"
                style="
                  text-decoration: none;
                  background-color: #5865f2;
                  padding: 9px;
                  color: white;
                  margin-left: 300px;
                "
                >Restablecer contraseña</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
        '''.format(usuario.usuarioNombre,link)) 

        return{
            "content": "se envio un correo con cambio de password"
        }


# & HAY UNA GRAN OBSERVACION OSEA YA NO SE PUEDE COLOCAR ACCESO DE APLICACIONES POCO SEGURO LO QUE HIZO GMAIL ES ANULARLO ESA OPCION X LO CUAL TOMO LA MEJOR OPCION DE QUE DEBEMOS LOGUEARNOS EN VERIFICACION EN 2 PASOS DESPUES DEBEMOS ENTRAR A CONTRASENIAS DE APLICACIONES QUE SE ENCUENTRA MAS ABAJITO DE VERIFICACION EN 2 PASSOS Y DEBEMOS GENERAR UNA CLAVE PARA EL DISPOSITIVOS ADECUADO

# Selecciona la aplicación y el dispositivo para los que quieres generar la contraseña de aplicación. Y ESA VA SER NUESTRA CLAVE APARTIR DE AHORA para k google pueda mandar mensaje al destino esa es la nueva forma para usar el gmail y el envio de los correos
