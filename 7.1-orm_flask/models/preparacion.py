from conexion_db import base_de_datos
from sqlalchemy import  types,Column
from sqlalchemy.sql.schema import ForeignKey

class PreparacionModel(base_de_datos.Model):
    __tablename__ ="preparaciones"

    preparacionId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)

    preparacionOrden=Column(name='orden',type_=types.Integer,nullable=False, default=1)

    preparacionDescripcion=Column(name='descripcion',type_=types.Text,nullable=False)

    # creando los foreign key
    receta=Column(ForeignKey(column='recetas.id',ondelete="RESTRICT"),name='recetas_id',type_=types.Integer,nullable=False)