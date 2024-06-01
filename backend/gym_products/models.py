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
          
class User(models.Model):
    userid = models.AutoField(primary_key=True)
    uname  = models.CharField(max_length=255)
    uphone = models.CharField(max_length=20)
    uemail = models.CharField(unique=True, max_length=255)
    udate  = models.DateField(auto_now = True) 
    class Meta:
        db_table = 'user'


class Sales(models.Model):
    saleid = models.AutoField(primary_key=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='productid')
    quantity = models.IntegerField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'sales'

# class UploadedFile(models.Model):
#     file = models.FileField(upload_to= 'uploads/')
#     uploaded_on = models.DateField(auto_now = True)

#     def __str__(self):
#         return self.uploaded_on.date()
