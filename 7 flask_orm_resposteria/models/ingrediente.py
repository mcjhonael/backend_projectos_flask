from conexion_db import base_de_datos
from sqlalchemy import Column,types,orm

# mira con atencion que esta clase que estamos creando que es IngredienteModel va heredar de base_de_datos su metodo Model le dira a flask que todos los atributos creado dentro de esta clase seran parte de la tabla

# por defecto la tabla creara con el nombre de IngredienteModel para cambiarlo de nombre usaremos un metodo privado __tablename__ y le colocar el nombre que deseas a esa tabla de preferencia en plural

# que es lo pasa detras cuando creamos las columnas dice hay el campo id si ok no entonces la creo igual hay campo nombre no la creo si ok = esto va pasar cada vez que inicializacion la app osea cada vez que python app.py asi
class IngredienteModel(base_de_datos.Model):
  __tablename__="ingredientes"
  # Esta el la primera manera en que podemos crear los campos como podemos ver es mas larga xk usamos la instancia de SQLAlchemy tanto para crear las columnas como para indicar el tipo de datos
  # id = base_de_datos.Column(base_de_datos.Integer, primary_key=True)
  # username = base_de_datos.Column(base_de_datos.String(80), unique=True, nullable=False)

# al momento de haber instalado la libreria flask-sqlalchemy tbm se instalo la libreria sqlalchemy x lo cual podemos usar sus metodos
# segunda forma que es mas corta para ello usamos de la misma libreria sqlalchemy el metodo Column para crear la columna de la tabla usamos tbm losq types es super para indicar que tipos de datos va ser dicho atributo
# si no usamos los types no nos podra brindar los tipos de datos que podemos usar con la autoayudaa aparte muy importante types nos brinda todos los tipos de datos de todos los gestores de base de datos x eso lo usamos

  ingredienteId=Column(name='id',type_=types.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
  
  ingredienteNombre=Column(name='nombre',type_=types.String(length=45),nullable=False,unique=True)

  #usa el metodo orm para podemos usar relationship 
  # creando el relationship se le coloca a las tablas que son padres a los hijos

  #creamos un campo ficticio con el nombre de la tabla hija y en plural ejm: recetas_ingredientes=orm.relationship('nombre_modelo_con_quien_deseamos_enlazar','nombre de la variable ficticia=nombre de la tablahija+nombredelatablapadreenplural en un camelcase') se le da lectura para indicar xk esta variable recetas_ingredientes va almacenar la relation creando en el padre un atributo del hijo que ara referencia a esa tabla hija x eso colocamos ese atributo hijo-padre

  #se usa el orm.relationship cuando la relacion es viceversa de uno a muchos considerando la tabla padre como uno 
  #se colocar una clave externa a la tabla secundaria que hace referencia a la principal

  #Muchos a uno coloca una clave externa en la tabla principal que hace referencia al elemento secundario. relationship()se declara en el padre, donde se creará un nuevo atributo de retención escalar:
  #esta clave recetas_ingredientes no va como un campo en la tabla si no que es de forma abstracta el atributo se crea con el nombre de la tabla hija pero en plural

  #las variables de los foreign son en singular y las variables de los relationship son en plural
  recetas_ingredientes=orm.relationship('RecetaIngredienteModel',backref='recetaIngredienteIngredientes',lazy=True)

  # este metodo sirve para personalizar lo que queria ver cuando haya print de una clase
  #este metodo privado permite ver el mensaje cuando imprimamos una clase en vez de salir unas cosas que no se entienden mejor que mande este mensaje
  def __str__(self):
      return 'el ingrediente es %s %d' % (self.ingredienteNombre,self.ingredienteId)