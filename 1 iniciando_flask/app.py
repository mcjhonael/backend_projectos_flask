# de la libreria flask importame la clase Flask

# recuerda q todas las clases son en mayusculas 

#toda clase debe ser instanciada

# python ya viene incluido con un  modulo VENV para crear entornos virtuales

# python3 -m venv name_virtual (usamos el -m para indicarle que usaremos un modulo)

# para poder desactivar el entorno virtual usamos el comando DEACTIVATE
from flask import Flask

#?creamos una instancia de la clase
#!__name__ muestra si el archivo en el cual se esta llamando a la clase Flask es el archivo principal del proyecto,esto se hace para evitar que la instancia de la clase Flask se pueda crear en otro lados(patron de disenio singletton)
#?singletton=patron de disenio que solamente permite instanciar un objeto de una clase osea solamente podemos instanciar 1 vez la clase
app=Flask(__name__) 

#si estamos en el archivo principal del proyecto nos imprimira __main__ caso contrario imprimira la ubicacion del archivo
# print(__name__) 

#^decorador @ => un patron de software que se utiliza para modificar el funcionamiento de una clase o una funcion en particular sin la necesidad de emplear otros metodos como la herencia(cosa que no se puede en una funcion comun y corriente)
#&mira esto cada vez que deseamos modificar una clase con el decorador tenemos que crear un metodo o funcion como respuesta al cambio que estamos haciendo algo asi es...
@app.route('/')
def incio():
    print('Hello! Worde!')
    return 'hola amiguitos'


#con este metodo ya podemos levantar nuestro servidor web siempre debe ir al final de todo el codigo si lo ponemos antes de algo no lo tomara en cuenta xk es el inicio de levantar el server
#el modo de debug permite que cuando add o modifiquemos algo en nuestro codigo el servidor tenga k reiniciarse y levantarse de nuevo
app.run(debug=True)
