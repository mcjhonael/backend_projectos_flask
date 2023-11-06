from conexion_db import base_de_datos
from sqlalchemy import Column,types
# usamos los FOREIGN KEY 
from sqlalchemy.sql.schema import ForeignKey


class PreparacionModel(base_de_datos.Model):
  __tablename__='preparaciones'
  preparacionId=Column(name='id',type_=types.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
  #cuando queremos colocar valores por defecto
  preparacionOrden=Column(name='orden',type_=types.Integer,default=1)
  
  preparacionDescripcion=Column(name='descripcion',type_=types.Text,nullable=False)

  # creando la ForeingKey con tal tabla recetas
  #recibe column= el nomre de la tabla y su columna
  # ondelete = que va pasar cuando se elimine el registro que esta apuntando preparaciones
    # Asi se crean las relaciones
    # en el parametro column => el nombre de la tabla y su columna
    # ondelete => indicar que accion debe de tomar el hijo (tabla donde esta ubicada la FK) cuando se elimine el registro de la fk
    # CASCADE => eliminar el registro de recetas y luego todos los registros ligados a esa receta
    # DELETE => se eliminar y dejara a las FK con el mismo valor aunque este ya no exista
    # RESTRINCT => restrige y prohibe la eliminacion de las recetas que tengan preparaciones (primero tendremos que eliinar las preparaciones y luego recien a la receta)
    # None => eliminalo y en las preparaciones setea el valor de la receta a Null
    # https://docs.sqlalchemy.org/en/14/core/constraints.html?highlight=ondelete#sqlalchemy.schema.ForeignKey.params.ondelete
    #tiene que tener el mismo tipo de la foreign key
    # ese foreign la convencion indica que debe llamarse el nombre de la tabla_atributo(recetas_id)
  receta=Column(ForeignKey(column='recetas.id',ondelete='RESTRICT'),name='recetas_id',nullable=False,type_=types.Integer)