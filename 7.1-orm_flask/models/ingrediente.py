from conexion_db import base_de_datos
from sqlalchemy import Column, types,orm

class IngredienteModel(base_de_datos.Model):
    __tablename__ ="ingredientes"
    
    ingredienteId=Column(name='id',type_=types.Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    
    ingredienteNombre=Column(name='nombre',type_=types.String(length=50),unique=True)

    # creamos los relationships para poder enlazar una comunicacion bidireccional de padres a hijos

    recetas_ingredientes=orm.relationship('RecetaIngredienteModel',backref='recetaIngredienteIngredientes',lazy=True)


    #cuando no usamos el metodo privado __str__ al imprimir esta clase ingredienteModel no dara el mismo ingredienteModel y una transaction k no se entiende para evitar eso usamos ese metodo para darlo algo de gracia
    
    def __str__(self):
        return "EL INGREDIENTE %s" % self.ingredienteNombre