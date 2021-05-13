from django.db import models
from django.db.models.deletion import SET_NULL

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    money=models.FloatField(null=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    fromPhone=models.CharField(max_length=200,null=True)
    toPhone=models.CharField(max_length=200,null=True)
    amt=models.FloatField(null=True)