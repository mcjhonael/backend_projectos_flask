# este archivo se encarga de modificar cuando la firma sea invalida (esta es la manera ordenada xk lo hacemos en un archivo aparte)

from flask import current_app
from flask_jwt import JWTError

# como este error es de ese tipo JWTError xk postman nos indica entonces nosotros podemos decir que el error es de ese tipo
# al decirle k va ser de ese tipo entonces eso nos ayuda a obtener k metodos tiene esa clase JWTError
# si no le colocamos el JWTError no pasa nada solamente es para decir k es de ese tipo igual k typescript
# code status http 401 no autorizado


def manejo_error_JWT(error: JWTError):
    print(error.status_code)
    print(error.description)
    print(error.headers)
    print(error.error)
    # print(current_app.config)
    message = ""
    if error.error == "Invalid token":
        message = "token invalida"
    elif error.error=="Authorization Required":
        message='Necesita una token para esta peticion'
    elif error.error=="Invalid JWT header":
        message='token sin el prefijo correcto'
    else:
        message="Error Desconocido"
    return {
        "message": message,
        "content": None
    }, error.status_code
