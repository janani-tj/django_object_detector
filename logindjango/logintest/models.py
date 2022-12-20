from django.db import models

# Create your models here.

from django.db import models
import datetime

class Video(models.Model):
    name= models.CharField(max_length=500)
    time=models.DateTimeField(default=datetime.datetime.utcnow)

