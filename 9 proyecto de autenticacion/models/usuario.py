from config.conexion_db import base_de_datos
from sqlalchemy import Column,types,orm

#por seguridad no es recomendable mandar el id al frontend
#para este caso se crea un identificador extra como seria el uuid xk crearlo para que asi el front no sea cuantos usuario hay en la bd
class UsuarioModel(base_de_datos.Model):
    __tablename__ ='usuarios'

    usuarioId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)

    usuarioNombre=Column(name='nombre',type_=types.String(length=50),nullable=False)

    usuarioApellido=Column(name='apellido',type_=types.String(length=50),nullable=False)

    usuarioCorreo=Column(name='correo',type_=types.String(length=50),nullable=False,unique=True)

    #no es unique xk varios user pueden tener la misma clave
    usuarioPassword=Column(name='password',type_=types.Text,nullable=False)

    usuarioTelefono=Column(name='telefono',type_=types.String(length=15),nullable=False)

    # creando relationship
    #recuerda que el foreignkey se crea en la tabla 
    #y el relationship se crea en el modelo
    #esto retornara el usuario que pertence esta tarea
    tareas=orm.relationship('TareaModel',backref='tareaUsuario',lazy=True)



#cuando aveces no podamos hacer consultas por el orm entonces usamos los ROW QUERIES  que son consultas puras a la bd
#en este proyecto vamos a usar json web token la cual tendra como finalidad 
# darle un tiempo de vida al iniciar session xk coloco mis credenciales y con json web token tengo un tiempo de vida de session no se 10min o lo k uno diga 
#en caso que caduque su session tambien podemos hacer para que renueve su session
#tambien veremos como incrytar la clave para que no sea visible para los demas y evitar problemas