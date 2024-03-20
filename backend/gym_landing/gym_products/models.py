from django.db import models
import os
from gym_landing.settings import MEDIA_ROOT
# Create your models here.
class Product(models.Model):
    id           = models.AutoField(primary_key=True)
    pname        = models.CharField(max_length=255)
    pdescription = models.TextField(blank=True, null=True)
    pprice       = models.DecimalField(max_digits=10, decimal_places=2)
    pstock       = models.IntegerField()
   
    class Meta:
        db_table = 'product'
    
    def __str__(self):
        return self.pname
   
    def imgs_path(self, filename):
        counter      = Product.objects.count()
        path         = os.path.join(MEDIA_ROOT, f'uploads/2') 
        filesCounter = 0
        pname        = self.pname  
        ppk          = counter + 1
        keyValue     = {
            'pname': pname, 
            'ppk'  : ppk
        }
        # if os.path.exists(path):
        #     for pathv2 in os.listdir(path):
        #        if os.path.isfile(os.path.join(path, path)):
        #            filesCounter += 1

        print(keyValue)

        return f'uploads/{counter+1}/{pname}'

    pimgpath     = models.FileField(upload_to = imgs_path, null = True)
      
         
        
class User(models.Model):
    userid = models.AutoField(primary_key=True)
    uname  = models.CharField(max_length=255)
    uphone = models.CharField(max_length=20)
    uemail = models.CharField(unique=True, max_length=255)
    udate  = models.DateField(auto_now = True) 
    class Meta:
        db_table = 'user'

# class UploadedFile(models.Model):
#     file = models.FileField(upload_to= 'uploads/')
#     uploaded_on = models.DateField(auto_now = True)

#     def __str__(self):
#         return self.uploaded_on.date()
