from conexion_db import base_de_datos
from sqlalchemy import Column,types,orm
from enum import Enum

# USAMOS Enum para poder tener solamente las opciones que deseamos nada mas
class EnumPorcion(Enum):
  personal='personal'
  mediano='mediano'
  familiar='familiar'

class RecetaModel(base_de_datos.Model):
  __tablename__='recetas'
  recetaId=Column(name='id',type_=types.Integer,primary_key=True,autoincrement=True,unique=True,nullable=False)
  recetaNombre=Column(name='nombre',type_=types.String(length=225))
  recetaPorcion=Column(name='porcion',type_=types.Enum(EnumPorcion))

# creando el relationship tabla padre a los hijos 
# este padre tiene 2 hijos
  # el relationship sirve para indicar los "hijos" que puede tener ese modelo con algunas relaciones previamente declaradas
    # backref => crea un atributo virtual en el otro modelo y sirve para que se pueda acceder a todo el objeto inverso
    # lazy => define como SQLAlchemy va a cargar la informacion adyacente de la base de datos
    # True / 'select' (default)=> carga toda la informacion siempre
    # False / 'joined' => solamente cargara cuando sea necesario (cuando se vaya a usar los atributos auxiliares)
    # 'subquery' => trabajara con todos los datos PEEERO en forma de una sub consulta
    # 'dynamic' => se puede agregar filtro adicionales. SQLAlchemy devolvera otro objeto dentro de la clase
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships


    # cuando queriamos acceder a preparaciones desde receta usabamos los join
    # este atributo se va crear en el otro modelo osea PreparacionModel para que cuando desde preparacion deseemos acceder a receta normal se pueda
    
    # mira el foreign key solamente sirve para q cuando le mandemos un id de receta si existe vacan y si no mandara error solamente para verificar que lo que mandes debe estar en la tabla receta si no es asi mandara erro

    #y gracias al relation nosotros podemos desde ese mismo modelo preparacionModel poermos traer los datos de receta es una cosa de lokos sin la necesidad de hacer los join

    #y tambien podria hacer lo mismo que desde mi RecetaModel puede acceder a mis preparaciones osea es viceversa una lokura

  preparaciones=orm.relationship('PreparacionModel',backref='preparacionRecetas',lazy=True)
  
  recetas_ingredientes=orm.relationship('RecetaIngredienteModel',backref='recetaIngredienteRecetas',lazy=True)
