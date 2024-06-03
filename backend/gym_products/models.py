import os
from django.db import models
from gym_landing.settings import MEDIA_ROOT
# Create your models here.
class Product(models.Model):
    id           = models.AutoField(primary_key=True)
    pname        = models.CharField(max_length=255)
    pbrand       = models.CharField(max_length=255, null = True, blank = True)
    pdescription = models.TextField(blank=True, null=True)
    pstatus      = models.CharField(max_length = 20)
    pcategory    = models.CharField(max_length = 50)
    pprice       = models.DecimalField(max_digits=10, decimal_places=2)
    pstock       = models.IntegerField()
    pimgspath    = models.FileField(upload_to = 'uploads/', null = True, blank = True)
 
    class Meta:
        db_table = 'product'
    
    def __str__(self):
        return str({"pid": self.id, "pname": self.pname,
                     "pdescription": self.pdescription,
                     "pprice": self.pprice, "pstock": self.pstock})      
          
class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=255)
    cphone = models.CharField(max_length=20)
    cemail = models.CharField(unique=True, max_length=255)
    cdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'customer'

class Sales(models.Model):
    saleid = models.AutoField(primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='productid')
    quantity = models.IntegerField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'sales'


class Shoppingcart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart'

