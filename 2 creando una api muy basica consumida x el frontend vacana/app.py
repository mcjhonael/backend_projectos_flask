#de la libreria flask importame la clase Flask

# El primer argumento es el nombre del módulo o paquete de la aplicación. __name__es un atajo conveniente para esto que es apropiado para la mayoría de los casos. Esto es necesario para que Flask sepa dónde buscar recursos como plantillas y archivos estáticos.

#? Para acceder a los datos entrantes en Flask, tiene que usar el objeto request. El objeto request contiene todos los datos entrantes de la solicitud o peticion, que incluye el mimetype, recomendante, dirección IP, datos sin procesar, HTTP y encabezados, entre otras cosas.

#<Request 'http://127.0.0.1:8080/' [GET]> recuerda que esto indica que es una instancia de la clase Request x lo cual podemos convertir los valores de una clase para acceder a sus atributos con el metodo request.__dict__ cosa que lo mismo pasa en Flask

#request es una instancia u objeto general de la clase Request la cual nos proporciona toda la informacion de la peticion o solicitud que esta realizando el frontend

#Flask analiza todos los datos de las solicitudes entrantes por ti y te da acceso a ellos a través de ese objeto global request 

# aqui esta la doc completa de Flask podemos buscar por flask.Request y saldra todos los metodos para la clase Request RECOMENDABLE XK EXPLICA TODOS DE FLASK CADA PASO
# https://flask.palletsprojects.com/en/2.1.x/api/?highlight=get_json#flask.Request

from flask import Flask,request

#libreria de acceso de los cors
from flask_cors import CORS

#instanciar la clase Flask
app=Flask(__name__)

#al hacerlo de esta manera le estamos dando todos los permisos a las rutas y methodos de cualquier lugar
#recuerda que toda clase siempre debe ser instanciada aqui no pasa eso xk le estamos dando todos los permisos a la app
CORS(app)


productos=[
    {
        "nombre":"palta fuerte",
        "precio":2.10
    },
    {
        "nombre":"cebolla",
        "precio":2.31
    },
    {
        "nombre":"tomate",
        "precio":1.2
    }
]

#uso de los decoradores para modificar un metodo de la clase Flask sin tener la herencia
#creamos nuestro 1er endpoint
@app.route("/")
def index():
    #siempre que vamos a responder al cliente tiene que ser por el return
    return {
        "message": "Bienvenido API",
        "content": "nada",
    }

#metodos permitidos para la ruta /productos
@app.route("/productos",methods=["GET","POST"])
def gestion_productos():
    #metodo get_json() sirve para visualizar todo la informacion que el usuario me esta enviando por el body
    #body es el cuerpo de la peticion donde el front adjunta toda la informacion que quiere enviar al backend
    #body se envia en formato JSON | multipart | text | xhtml
    #request.method =brindara el tipo de metodo por el cual se esta realizando la solicitud aparte tenemos mucha mas informacion de la peticion ejm: request.method,request.headers,request.endpoint,etc 
    # recuerda que siempre en una solicitud vamos a encontrar methods - headers - body 
    print(request.method)

    # HACEMOS UNA VALIDACION PARA VER COMO DEBE RESPONDER MI RUTA A DIFERENTES METHODS
    if request.method=="POST":
        producto=request.get_json()
        productos.append(producto) 
        
        return{
            "content":producto,
            "message":"Producto creado exitosamente"
        },201
    print(productos)
    return{
        "content":productos,
        "message":None
    },200

#el parametro debe tener el mismo nombre del metodo a responder como argumento
#para poder usar parametros dentro de las rutas entonces colocamos <> especificando el tipo_dato:name_variabble
@app.route("/producto/<int:id>",methods=["GET","PUT","DELETE"])
def gestion_producto(id):
    #aqui verificamos si el id que manda el user esta dentro de nuestra lista de productos si es asi continuamos y si no paramos
    total_productos=len(productos)
    
    if id<total_productos:
        if request.method=="GET":
            return{
                "content":productos[id],
                "message":None
            },200

        elif request.method=="PUT":
            data=request.get_json()
            productos[id]=data
            return{
                "message":"Producto Actualizado",
                "content":productos[id],
            },201

        elif request.method=="DELETE":
            del productos[id]   
            return{
                "content":None,
                "message":"Producto eliminado exitosamente"
            },200
    else:
        return{ 
            "message":"Product no encontrado",
            "content":None
    },404

if __name__ == "__main__":
    app.run(debug=True,port=8000)

    # cuando uso evento yo no puedo guardarlo en una variables para ello tendria k crear una function para poder reutilizar ese metodo y usarlo en cualquier parte
    
#   const enviarFormulario=function(){
#     enviarFruta.onclick =function(e){
#         e.preventDefault();
#         console.log("holitas");
#         console.log(inputNombre.value);
#         fetch(BASE_URL+"/frutas",{
#             method:"POST",
#             headers:{
#                 "Content-Type":"application/json"
#             },
#             body:JSON.stringify({
#                 nombre:inputNombre.value,
#                 precio:+inputPrecio.value
#             })
#         })
#     }
# }

# un cachito
# Después de desarrollar su aplicación, querrá ponerla a disposición del público para otros usuarios. Cuando está desarrollando localmente, probablemente esté utilizando el servidor de desarrollo integrado, el depurador y el recargador. Estos no deben ser utilizados en la producción. En su lugar, debe usar un servidor WSGI dedicado o una plataforma de alojamiento, algunos de los cuales se describirán aquí.

#?una super informacion para k el servidor se reinicie solo y no estar levantandolo de nuevo necesitamos instalar estas 2 librerias super buenas
# pip install -U py-mon
# pip install watchdog // para k escuche los cambios

# y le damos a correr con pymon app.py