from distutils.command.upload import upload
from email.mime import image
from django.db import models

# Create your models here.
class Person(models.Model):
    id = models.AutoField(primary_key = True)
    image = models.ImageField(upload_to = 'images/')

class RegisteredChild(models.Model):
    num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    mobile_num = models.CharField(max_length=15)
    image = models.ImageField(upload_to = 'registered_images/')


    