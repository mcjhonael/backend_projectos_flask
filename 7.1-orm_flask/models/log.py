from conexion_db import base_de_datos
from sqlalchemy import Column,types
from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey

class LogModel(base_de_datos.Model):
    __tablename__='logs'

    logId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)

    logFecha=Column(name='fecha',type_=types.DateTime(),default=datetime.utcnow)

    logRazon=Column(name='razon',type_=types.Text)
