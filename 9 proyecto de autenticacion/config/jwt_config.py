from os import environ
#?los segundos, minutos y horas son expresados en segundos si o si
#los dias son en dias
from datetime import timedelta

def JWTSecret(app):
    # este clave secrete es nuestra firma para el token
    app.config['SECRET_KEY']=environ.get('JWT_SECRET')
    #como parametro puede recibir days, seconds, microseconds, milliseconds, minutes, hours, weeks
    app.config['JWT_EXPIRATION_DELTA']=timedelta(minutes=180)

    #esto sirve para cambiar en vez de mandar el username x el body mejor que se llame email y ya no correo o username
    app.config['JWT_AUTH_USERNAME_KEY']='email'

    #cual va ser la ruta cuando queramos hacer login x defecto es /auth lo vamos a cambiar
    #osea cuando hagamos /login sera el proceso de autenticacion (ya lo verifique y si es verdad el /login se considero como autenticacion)
    #osea lo que paso es que normalmente se crea automaticamente una ruta /auth para la autenticacion y a esa ruta me mandar la token en caso que las credenciales coincidan
    #pero yo habia creado una nueva ruta /login para que considere q sea su numera ruta
    app.config['JWT_AUTH_URL_RULE']='/login'

    #Esta sirve para poder modificar el prefijo de la token ya que por defecto es JWT y el otro modo no sirve de esa manera
    app.config['JWT_AUTH_HEADER_PREFIX']='BEARER'
    return app


    #&que va cuando el usuario este realizando un proceso y termine la session que debe hacer el usuario en este caso para continuar xk se quedo en la mitad 
    #^lo que hace el frontend es obtener el iat y exp convertirlo a fecha new Date(iat) new Date(exp) luego restarlas las fechas para saber cuanto tiempo nos queda de session luego colocar un cronometro para que cuando le falte 1 minuto lanze un mensaje indicando k le falta poco para terminar su session con un boton que diga desea continuar la session
    #?lo que ara ese boton sera un peticion al servidor de /refresh lo que ara este endpoint es refrescar la session entonces en el servidor lo verificara y si todo esta bien mandara una nueva token generada access_token:valor