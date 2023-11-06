from config.conexion_db import base_de_datos
#types mostrara todos los tipos de datos genericos de todas las bd
#UniqueConstraint podemos hacer de la siguiente manera osea no se puede repetir una conjugacion osea titulo y estado osea tarea1  por_hacer tarea2 haciendo tarea3 finalizado asi osea no se puede volver a hacer alguna otra conjuncion con esos valores xk seria un UniqueConstraint abajo lo hago asi
from sqlalchemy import Column,types,UniqueConstraint
from datetime import datetime
#de esta manera podemos usar unicamente los dialectos permitidos de nuestro postgres y asi tbm en mysql
# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.schema import ForeignKey
from enum import Enum

class EnumEstado(Enum):
    POR_HACER='por_hacer'
    HACIENDO='haciendo'
    FINILIZADO='finilizado'


class TareaModel(base_de_datos.Model):
    __tablename__ ="tareas"

    tareaId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)

    tareaTitulo=Column(name='titulo',type_=types.String(length=100),nullable=False)

    tareaDescripcion=Column(name='descripcion',type_=types.Text)

    tareaFechaCreacion=Column(name='created_at',type_=types.DateTime,default=datetime.now)

    tareaTags=Column(name='tags',type_=types.ARRAY(types.Text))

    tareaEstado=Column(name='estado',type_=types.Enum(EnumEstado),nullable=False)

    tareaImagen=Column(name='imagen',type_=types.Text,nullable=True)

    #pero tambien podrias decir titulo unique y estado unique usamos el UniqueConstraint para hagarralo en conjunto mejor
    # UniqueConstraint('titulo','estado')

    # creando la relacion
    usuario=Column(ForeignKey(column='usuarios.id',ondelete='RESTRICT'),name='usuario_id',type_=types.Integer,nullable=False)