##LA FINALIDAD DE ESTE PROYECTITO ES HACER UN CRUD NIVEL BASICO con BASE DE DATOS Y VEREMOS COMO FUNCIONA ESO

# C = reate = POST 
# R = ead = GET = cuando queremos seleccionar un product, listarlo, ordenarlo
# U = pdate = PUT | PATCH
# D = elete = DELETE

# ALGUNOS CODIGO DE ESTADO RESPUESTA HTTP (ESTAS SON LAS RESPUESTAS QUE VA A MANDAR EL SERVIDOR AL FRONTEND)
# response = respuesta
# request = peticion

##RESPUESTAS SATISFACTORIAS
#200 OK = La solicitud tuvo éxito. 
# El significado del resultado de "éxito" depende del método HTTP:
# GET: el recurso se ha obtenido y transmitido en el cuerpo del mensaje.
# HEAD: Los encabezados de representación se incluyen en la respuesta sin ningún cuerpo de mensaje.
# PUT | POST: El recurso que describe el resultado de la acción se transmite en el cuerpo del mensaje.
#201 Created = La solicitud se realizó correctamente y, como resultado, se creó un nuevo recurso. Esta suele ser la respuesta enviada después de POST las solicitudes, o algunas PUTsolicitudes.
# 204 No Content = No hay contenido para enviar para esta solicitud, pero los encabezados pueden ser útiles

##RESPUESTAS DE DIRECCINAMIENTO
# --------

##ERRORES DE CLIENT
# 400 Bad Request  Esta respuesta significa que el servidor no pudo interpretar la solicitud dada una sintaxis inválida. mala peticion al escribirlo
# 404 Not Found = El servidor no pudo encontrar el contenido solicitado. Este código de respuesta es uno de los más famosos dada su alta ocurrencia en la web.
# 405 Method Not Allowed = El método solicitado es conocido por el servidor pero ha sido deshabilitado y no puede ser utilizado

##ERROR DE SERVIDOR
#que nuestra logica estuvo mal x lo consecuente no se pudo dar un respuesta correctamente
#500 Internal Server Error = El servidor ha encontrado una situación que no sabe como manejarla.


#^flask-mysqldb= libreria que permite conectar desde python a mysql si o si para darle la configuracion osea es un conector 

# de la libreria flask importame la clase Flask ya que las clases son siempre en mayusculas
from flask import Flask,request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from funciones import areaConfigDB

#cargar las variables de entorno
load_dotenv()

# instanciamos la clase Flask y le pasamos el __name__ para indicarle que este es el archivo principal (app.py)
#area de instancia
app=Flask(__name__)
#contiene todas las variables que estoy usando en mi proyecto de flask
# print(app.config)

#muestra todo un diccionario de todas las variables de entorno de nuestra maquina hasta las que hemos creado en .env y las que vamos a crear super!!
# print(environ)

#config de var de mysql para flask
#crear las credenciales a nuestra aplicacion
#area de configuracion en este metodo aparte tenemos la configuracion completa
areaConfigDB(app)

#instanciar la libreria MySQL pasandole la applicacion
# lo instanciamos despues k mysql necesita tener la configuracion 1ro
mysql=MySQL(app)


@app.route("/")
def home():
    return "Holiii"

# metodo para insertar 1 elemento y lista 1 elemento
@app.route('/departamentos',methods=['GET','POST'])
def inicio():
    print(request.method)
    if request.method=='GET':
        #hace una coneccion a nuestra bd x medio de un cursor
        #cursor un puntero que esta apuntando a nuestra base de datos
        cur=mysql.connection.cursor()

        #despues de apuntar a nuestra base de datos ejecutamos la sentencia
        cur.execute('SELECT * FROM DEPARTAMENTOS')

        #y ese resultado se guardara en el curso y para acceder a su resultado con metodo
        resultado=cur.fetchall()

        #lo que retorna sera una tuplas de tuplas x lo cual debemos recorrerlo
        # print(resultado)
        departamentos=[]
        for departamento in resultado:
            departamentos.append(
                {
                    'id':departamento[0],
                    'nombre':departamento[1]
                }
            )
        return{
            'message':None,
            'content':departamentos
        },200
    elif request.method=="POST":
        
        data=request.get_json()

        cur=mysql.connection.cursor()

        #formateo de string super bueno
        # https://www.learnpython.org/es/String%20Formatting
        cur.execute("INSERT INTO DEPARTAMENTOS(NOMBRE) VALUES('%s')" % data['nombre'])
        #para que perdure en la base de datos usamos el commit
        mysql.connection.commit()
        return{
            'message':'departamento creado exitosamente',
            'content':data
        },201
    else:
        return{
            "message":"metodo no encontrado",
            "content":None
        },405 

#este es metodo para traer 1 registro elimianr 1 y actualizar 1
# doc de python para mysql
# https://peps.python.org/pep-0249/
@app.route('/departamento/<int:id>',methods=['GET','DELETE','PUT'])
def departamento(id):
    if request.method=='GET':
        cur=mysql.connection.cursor()
        cur.execute(f'SELECT * FROM DEPARTAMENTOS WHERE id={id}')
        # cur.execute("SELECT * FROM DEPARTAMENTOS WHERE ID=%d" % id)
        respuesta=cur.fetchall()
        departamento=[]
        for depa in respuesta:
            departamento.append(
                {
                    'id':depa[0],
                    'nombre':depa[1]
                }
            )
        return{
            'content':departamento,
            'message':None
        },200
    #no puedo hacer un delete xk tengo que colocar en base de datos esto
    #para poder hacer la eliminacion si no no se podra hacerlo
    #en mysql hay que especificar el tipo de eliminacion que deseamos hacer con las claves foraneas
    #FOREIGN KEY (ciudad) REFERENCES clientes(ciudad) ON DELETE CASCADE
    elif request.method=='DELETE':
        cur=mysql.connection.cursor()
        cur.execute(f"DELETE FROM PERSONALES WHERE ID={id}")
        mysql.connection.commit()
        return {
            'message':"exitosamente eliminado",
            "content":None
        }
    elif request.method=="PUT":
        data=request.get_json()
        print(data)
        cur=mysql.connection.cursor()
        cur.execute(f"UPDATE PERSONALES SET NOMBRE='{data['nombre']}' WHERE ID={id}")
        mysql.connection.commit()
        return{
            "content":data,
            "message":"Persona actualiza exitosamente"
        },201

if __name__=='__main__':
    app.run(debug=True,port=5000)

#para poder obtener todos las librerias que hemos usado en nuestro entorno virtual
#pip freeze > requirements.txt

#cuando queramos instalarlo usaremos asi
#instalame todos los requerimientos del archivo requirements.txt 
#pip install -r requirements.txt