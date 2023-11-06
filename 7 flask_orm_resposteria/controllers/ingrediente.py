from flask_restful import Resource, reqparse
from conexion_db import base_de_datos
from sqlalchemy.exc import DataError, IntegrityError

#import model
from models.ingrediente import IngredienteModel
from models.log import LogModel

#LA TAREA ES REALIZAR UN CRUD DE INGREDIENTES

# lo mejor es que api flask-restful nos brinda un super validador de parametros

# lo normal seria recibir los parametros del front pero el unico problema es que si usamos request.get_json() recibe todo el body que nos estan mandando informacion necesaria e informacion basura x lo cual usamos serializador que seria un validador de que datos puede mandar el front

# serializador => elemento que convierte los parametros que me envia el fronted para tener un uso correcto en el backend

# recuerda que reqparse es una clase de flask_restful y tiene muchos metodos por lo cual instanciamos RequestParser()
# de esta manera ya tenemos nuestro serializador inicializado
serializador = reqparse.RequestParser()

# ahora tenemos que definir los argumentos que necesitamos para interactuar  con nuestra clase podemos args y kwargs
# args = solamente recibe el valor aqui se almancenan las tuplas
# kwargs = reciben el nombre de la variable y su valor y aqui los diccionarios
# utilizamos este serializador para argumento si tengo 5 argumentos que pasar entonces 5 serializadores ya que funcionan como validador
serializador.add_argument(
    'nombre',  # es obligatorio que me pases la variable nombre
    type=str,  # que esa de tipo string
    required=True,  # obligatorio
    location='json',  # me lo pasas x el json osea x el body
    # mensaje cuando no cumplas con pasar el parametro se mostrara solamente cuando el args sea requerido
    help='Falta el nombre'
)

# ?ojo cada vez que yo ingrese a la ruta recien el controlador saltara y si no ingreso pues nel pastel


class IngredientesController(Resource):
    # mostrar todos los ingredientes
    def get(self):
        # list de instancias de la clase
        # data=IngredienteModel.query.all()

        # SI NO ENCUENTRA DATOS DEVOLVERA UN ARREGLO VACIO
        # retorna como un arreglo de instancias de registro de la base de datos que no se puede iterar osea no entendible

        # cuando no lo recorremos este arreglo nos nuestra puras instancias de las clases IngredienteModel
        
        # pero cuando lo recorremos ya podemos verlo un poco mejor con el metodo __str__ que tiene la clase
        ingredientes = base_de_datos.session.query(IngredienteModel).all()

        # cuando mostramos de manera grupal (list) nos manda la instancia del modelo
        # print(ingredientes)

        resultado = []
        # cuando mostramos de manera individual entonces nos mostrar deacuerdo al __str__ del modelo
        for ingrediente in ingredientes:
            # el metodo __dict__ permite optener todo un diccionario de los atributos de dicha clase
            # print(ingrediente.__dict__)
            # recuerda que la data que llega yo no puedo modificarlo solamente tengo k hacer una copia y recien poder hacer las cosas

            # cuando solo mostramos ingrediente nos la la instancia del objeto ingredienteModel x lo cual para convertirlo a un json serializado y entendido usamos .__dict__
            # el .__dict__ lo convertira en un json serializado y entendido osae me retorna la direccionde memoria de esa instancia y sus atributos id y nombre
            # x lo cual eliminamos el campo de direccion de memoria xk no nos sirve nada
            print(ingrediente.__dict__)
            ingrediente_dicc = ingrediente.__dict__
            del ingrediente_dicc['_sa_instance_state']
            resultado.append({
                "id": ingrediente.ingredienteId,
                "nombre": ingrediente.ingredienteNombre
            })

        return {
            "content": resultado,
            "message": None
        }

    # crear un ingrediente
    # con este metodo nosotros debemos 1ro validar el argumento antes de colocarlo en la base de datos
    def post(self):
        # valida en base a los argumentos indicados si esta  cumpliendo o no el frontend con pasar dicha informacion si no cumple no seguira en el siguiente codigo si no que parara
        # luego de validar la informacion lo va capturar argumento que estamos necesitando por lo cual ya no es necesario para flask_restful request.get_json() no sirve xk este permite traer todos los datos del body y para filtrar tendriamos que hacer muchos if y esa vainas
        # ya con esto serializador ya que contamos con los datos estos listos para poder guardar los datos en la base de datos

        # con este metodo solamente vamos a capturar los argumento que se esta enviando nada del front
        data = serializador.parse_args()
        try:
            # devuelve una instancia de la clase del valor ingresado(<ingredienteModel 2>)
            # aqui estamos agregando los datos dentro del modelo como parametro
            # instanciamos la clase IngredienteModel para poder pasarle como parametro el valor que hemos capturado gracias al validados serializador

            # una vez que ya hemos obtenido la data debemos crear una nueva instancia como un registro
            # ingrediente=IngredienteModel()
            # ingrediente.ingredienteNombre=data['nombre']  
            # print(ingrediente)
    

            # otra forma de crear un registro como objeto seria
            nuevoIngrediente = IngredienteModel(
                ingredienteNombre=data['nombre'])

            # mira que esto va saltar xk esta variable esta guardando una instancia de la clase IngredienteModel x lo cual dentro de esa clase va saltar def __str__
            # print(nuevoIngrediente)

            # inciando la transaccion para conservar los cambios y guardarlos en la base de datos
            # cuando no cumpla las condiciones o las validaciones es aqui cuando el valor errore intenta entrar a la base de datos y falla y se va al except no se guarda xk fallo
            base_de_datos.session.add(nuevoIngrediente)
            # si el campo que estams enviando no cumple entonces no se podra hacer commit y saltara la excepcion x lo cual debemos manejarlo
            base_de_datos.session.commit()

            # tengo una instancia de la clase x lo cual puedo acceder asus atributos con el .
            # CUIDADO PARECE QUE CUANDO CREAMOS UN NUEVO REGISTRO NO PODEMOS USAR EL METODO __dict__
            print(nuevoIngrediente)
            # print(nuevoIngrediente.__dict__)
            # print(nuevoIngrediente.ingredienteNombre)

    # por que creamos este json xk nuevoIngrediente es una instancia de la clase x lo cual para acceder a sus atributos podemos usar el . por ende cuando hacemos una creacion debemos mandarle al front un json indicando el dato creado
            json = {
                "id": nuevoIngrediente.ingredienteId,
                "nombre": nuevoIngrediente.ingredienteNombre
            }
            error = None
            return{
                'message': "Ingrediente creado Exitosamente",
                'content': json
            }, 201
        except DataError as err:
            error = err
            return{
                "message": "Error al ingresar el ingrediente"
            }, 500
        except IntegrityError as err:
            error = err
            return{
                "message": "ese ingrediente ya existe"
            }, 500
        except Exception as err:
            error = err
            return{
                "message": "Error Desconocido"
            }, 500
        finally:
            if error is not None:
                base_de_datos.session.rollback()
                nuevoLog = LogModel()
                # como es un tipo de clase entonces casi siempre tiene este atributo .args que tiene una lista de las instancias de los tipos de errores que han oucrrido
                # print(type(error))
                # La cláusula except puede especificar una variable después del nombre de la excepción. La variable está vinculada a una instancia de excepción con los argumentos almacenados en instance.args. Por conveniencia, la instancia de excepción define __str__() para que los argumentos se puedan imprimir directamente sin tener que hacer referencia a .args. También se puede crear una instancia de una excepción antes de generarla y agregarle los atributos que desee.
                # error= una instancia de la clase DataError
                # error.args = alamacena el tipo de erro que ocurrio en una lista []
                # erro.args.[0]= brinda el contenido del error
                print(error.args[0])
                nuevoLog.logRazon = error.args[0]
                base_de_datos.session.add(nuevoLog)
                base_de_datos.session.commit()


class IngredienteController(Resource):
    # mostrar un 1 ingrediente especifico
    def get(self, id):
        #1 forma de hacerlo
        # resultado=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==id).first()

        # me retorna la sentencia sql SELECT * FROM INGREDIENTE WHERE INGREDIENTE.ID=ID y cuando le add .first() este metodo me dice retorna solamente 1 coincidencia
        # y me retorna una instancia del modelo a buscar no serializado
        #2da forma de hacerlo
        resultado2 = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        # print(resultado)
        print('+++++++++++++++++++++++++++')
        print(resultado2)
        if resultado2 is not None:
            data = resultado2.__dict__
            del data['_sa_instance_state']
            return {
                "content": data,
                "message": None
            }
        else:
            return{
                "message": "NOT FOUND INGREDIENT"
            }, 404

    # actualizar 1 ingrediente
    def put(self, id):
        data = serializador.parse_args()
        ingrediente = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente is None:
            return {
                "message": "Ingrediente no existe",
                "content": None
            }, 404

        ingrediente.ingredienteNombre = data['nombre']
        respuesta = ingrediente.__dict__.copy()
        base_de_datos.session.commit()
        del respuesta['_sa_instance_state']
        print(respuesta)
        return{
            "content": respuesta,
            "message": "ingrediente ya existe"
        }

    # eliminar 1 ingrediente
    # en este momento que deseamos eliminar un id que no se encuentra en la base de datos por lo cual debemos
    def delete(self, id):

        # retorna el numero de cuentas que fueron eliminados x ese campo
        # base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==id).delete()
        # eliminar=base_de_datos.session.query(IngredienteModel).filter_by(ingredienteId=id).first()
        base_de_datos.session.query(IngredienteModel).filter(
            IngredienteModel.ingredienteId == id).delete()

        # guardar los cambios
        base_de_datos.session.commit()
        return {
            "message": "Ingrediente eliminado Exitosamente",
            "content": None
        }, 204
        # 204 la operacion fue exitosa pero no hay datos a mostrar


# ahora crearemos un buscador x nombre de ingrediente pero esto se para como argumento x el metodo get ya no como el anterior que era por parmetro entonces x eso creamos diferente serializador
serializadorFiltro = reqparse.RequestParser()
serializadorFiltro.add_argument(
    'nombre',
    type=str,
    required=True,
    location='args',
    help='no se encontro buscador'
)


class FitroIngredientesController(Resource):
    def get(self):
        filtro = serializadorFiltro.parse_args()
        # ?esta consulta no sirve xk ingrediente no se puede repetir opera solo traeria 1 ingrediente k cumpla con todas las caracteristicas del nombre si te equivocas en algo entonces esto no funcionara
        # ?filtros=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteNombre==filtro).all()

        # ^ahora usaremos un metodo para poder obtener todos los valores que tengan parecido al nombre osea un like
        # ^podemos filtrar en las consultas asi
        # ? el % significa cero uno o varios caracteres
        # osea que ejmp p% = traer todo que empieze con la letra p enseguida de cualquier caracter
        # %p = traer todos que empiezen con cualquier caracter y termine si o si con la letra p
        # %p% = traer todos que empieze con cualquier caracter luego el p y al final cualquier caracter (osea traer todas las coincidencia)
        # si no pongo el all() me traera la consulta que hubieramos hecho en SQL
        # la manera normal seria esto ahora debemos adecuarda a nosotros
        # ingredientes=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteNombre.like('%elizabeth%')).all()
        # resultado=[]
        # for ingrediente in ingredientes:
        #     ingredienteDicc=ingrediente.__dict__.copy()
        #     del ingredienteDicc['_sa_instance_state']
        #     print(ingredienteDicc)
        #     # json={
        #     #     'id':ingredienteDicc['ingredienteId'],
        #     #     'nombre':ingredienteDicc['ingredienteNombre']
        #     # }
        #     resultado.append(ingredienteDicc)

        # primer forma
        # Para aplicar un filtro a una consulta, lo que sería la cláusula WHERE de SQL, puedes llamar a los métodos filter_by(keyword) o filter():
        resultado = base_de_datos.session.query(IngredienteModel).filter(
            IngredienteModel.ingredienteNombre.like('%{}%'.format(filtro['nombre']))).all()

        # segunda forma
        # retorna una lista de tuplas = a type Row
        # al usar with_entities nos retorna una lista de objetos de la clase Row
        # resultado=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteNombre.like('%{}%'.format(filtro['nombre']))).with_entities(IngredienteModel.ingredienteNombre).all()
        print('filtro {}'.format(filtro))

        # este es un resultado de type row por lo cual no es un json serializado
        print(f'resultado: {resultado}')

        resultado_final = []

        # primera forma de hacerlo
        for registro in resultado:
            ingrediente_dicc = registro.__dict__.copy()
            del ingrediente_dicc['_sa_instance_state']
            print(ingrediente_dicc)
            resultado_final.append(ingrediente_dicc)
        return{
            "message": None,
            "content": resultado_final
        }

        # segunda forma de hacerlo
        # for registro in resultado:
        #   print(type(registro))
        #   #lo convierte en un json serializado trabaja para los types Row ._asdict()
        #   print(registro._asdict())
        #   resultado_final.append(registro._asdict())
        # return{
        #   "message":"aqui filtro",
        #   "content":resultado_final
        # }


# try:
#   pass
# # crear la exepcion
# except:
#   pass
# aqui la consumnes
#   raise()
