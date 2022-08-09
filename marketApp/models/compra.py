from django.db import models
from .user import User

class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(User, related_name='cliente', on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    