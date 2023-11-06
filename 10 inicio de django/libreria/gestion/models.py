from django.db import models

#?la doc para los types de campo y para los parametros que pueden llevar ellos  https://docs.djangoproject.com/en/4.0/ref/models/
#?creacion de los modelos ejmp https://docs.djangoproject.com/en/4.0/topics/db/models/
class ProductoModel(models.Model):
    __tablename__='productos'
    productoId=models.AutoField(db_column='id',primary_key=True,unique=True,null=False)

    productoNombre=models.CharField(db_name='nombre',max_length=40,null=False)

    productoPrecio=models.models.DecimalField(db_name='precio', max_digits=5, decimal_places=2)