from django.db import models

# Create your models here.
class Product(models.Model):
    id           = models.AutoField(primary_key=True)
    pname        = models.CharField(max_length=255)
    pdescription = models.TextField(blank=True, null=True)
    pprice       = models.DecimalField(max_digits=10, decimal_places=2)
    pstock       = models.IntegerField()

    class Meta:
        db_table = 'product'

 
class User(models.Model):
    userid = models.AutoField(primary_key=True)
    uname  = models.CharField(max_length=255)
    uphone = models.CharField(max_length=20)
    uemail = models.CharField(unique=True, max_length=255)
    udate  = models.DateField(auto_now = True) 
    class Meta:
        db_table = 'user'

class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateField(auto_now = True)

    def __str__(self):
        return self.uploaded_on.date()
