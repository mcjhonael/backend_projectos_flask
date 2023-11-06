from conexion_db import base_de_datos
from sqlalchemy import Column,types,orm
from enum import Enum


class EnumPorcion(Enum):
    PERSONAL="personal"
    MEDIANA="mediana"
    FAMILIAR="familiar"

class RecetaModel(base_de_datos.Model):
    __tablename__ = "recetas"
    
    recetaID=Column(name="id",type_=types.Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)

    recetaNombre=Column(name="nombre",type_=types.String(length=50),unique=True,nullable=True)

    recetaPorcion=Column(name='porcion',type_=types.Enum(EnumPorcion))

    # creando los relationship

    preparaciones=orm.relationship('PreparacionModel',backref='preparacionRecetas',lazy=True)

    recetas_ingredientes=orm.relationship('RecetaIngredienteModel',backref='recetaIngredienteRecetas',lazy=True)

    #ojo ningun atributo de los relationships mas que todo el backref deben ser iguales si no lanzara mucho errores cuidado!!