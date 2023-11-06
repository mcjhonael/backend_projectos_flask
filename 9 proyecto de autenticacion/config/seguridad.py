# cuando un archivo se encuentra en la misma carpeta es recomendable usar el . si si no lo colocamos python podria considerarlo como si fuera una libreria
from .conexion_db import base_de_datos
from models.usuario import UsuarioModel
from bcrypt import checkpw


class Usuario():
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return 'Usuario con el id=%s y el username=%s' % (self.id, self.username)


"""Se encarga de validar que el usuario esta correctamente autenticado"""
# ?va indicar si es o no el usuario su funalidad es retorna algo
# & cuando las credenciales coincidan con las de la bd entonces lo que retornara sera una access_token y cuando no coincidan entonces retornara un dict con la description del error, el error y el estado del error
# {
#     "description": "Invalid credentials",
#     "error": "Bad Request",
#     "status_code": 401
# }


def autenticador(username, password):
    """funcion encargada en mi JWT de validar las credenciales usuario y clave, valida si son ingresadas correctamente y luego valida si es el usuario"""
    if username and password:
        # si mando el usuario y la clave entonces debemos validar en la bd si existe
        usuario = base_de_datos.session.query(
            UsuarioModel).filter_by(usuarioCorreo=username).first()
        if usuario:
            hash = bytes(usuario.usuarioPassword, 'utf-8')
            pwdBytes = bytes(password, 'utf-8')
            if checkpw(pwdBytes, hash) is True:
                return Usuario(usuario.usuarioId, usuario.usuarioCorreo)
    return None

# este metodo va saltar cuando nosotros ingresemos a la ruta usuario y le pasemos la token en los headers


#cuando yo kiera entrar ala ruta /usuario con la token los erorores van a saltar pero si las credenciales estan bien igual va saltar el payload en ese momento
def identificador(payload):
    '''esta funcion sirve para que una vez el usuario envie la token y quiera realizar una peticion a una ruta protegida esta funcion sera encargada de identificar a dicho usuario y devolver  su informacion'''
    # print(payload)
    # print(payload.get('identity'))


    #como hemos modificado @jsonwebtoken.jwt_payload_handler del archivo app.py osea hemos modificador el payload entonces ya no hay ese atributo identity si no que lo hemos cambiado x usuario 
    # usuarioId = payload.get('identity')
    #y ahora si funciona todo ok magia y si no modificamos el payload entonces seria igualcon el identity
    usuarioId=payload.get('usuario').get('id')

    # ahora buscamos a al usuario en la bd y lo mostramos en un dic
    usuarioEncontrado = base_de_datos.session.query(
        UsuarioModel).filter_by(usuarioId=usuarioId).first()

    if usuarioEncontrado:
        usuarioDict = usuarioEncontrado.__dict__
        # print(usuarioDict)

        # este retorno se va guardar en una variable llamada current_identity x lo cual lo usaremos en el controlador del usuario
        return usuarioDict
    return None
