from conexion_db import base_de_datos
from sqlalchemy import Column
from sqlalchemy.types import Integer,DateTime,Text
from datetime import datetime


class LogModel(base_de_datos.Model):
  __tablename__='logs'

  logId=Column(name='id',type_=Integer,primary_key=True,autoincrement=True,unique=True,nullable=False)

# https://docs.python.org/es/3/library/datetime.html#datetime.datetime.utcnow
# http://www.codexexempla.org/articulos/2008/llamada_referencia.php
  logFecha=Column(name='fecha',type_=DateTime(),default=datetime.utcnow)
  
  logRazon=Column(name='razon',type_=Text)
  