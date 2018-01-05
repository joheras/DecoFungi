from django.db import models

# Create your models here.
class ImagenyPrediccion(models.Model):              #Para el fichero ZIP
    id = models.AutoField(primary_key=True);
    nombreImagen=models.CharField(max_length=100)
    prediccion = models.CharField(max_length=4)
    nombre= models.CharField(max_length=100)

class ObjetoFungi(models.Model):#PARA ALMACENAR EN LA BD
    id = models.AutoField(primary_key=True); #ES LA CLAVE PRIMARIA QUE SE VA AUTOGNERANDO
    name = models.CharField(max_length=100)
    dye=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    prediction = models.CharField(max_length=4)
    description=models.CharField(max_length=1000)