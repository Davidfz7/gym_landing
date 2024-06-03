from gym_products.models import Product, Customer, Sales
from rest_framework import serializers
class ProductSerializer(serializers.Serializer):

    id           =serializers.IntegerField(required = False) 
    pname        = serializers.CharField(max_length = 255)
    pbrand       = serializers.CharField(max_length = 255)
    pdescription = serializers.CharField()
    pstatus      = serializers.CharField()
    pcategory    = serializers.CharField()
    pprice       = serializers.DecimalField(max_digits=10, decimal_places= 2)
    pstock       = serializers.IntegerField()
    pimgspath    = serializers.FileField(required = False, allow_null = True)

    #With this method we de-serialize(kind of parsing) the data into a Product object(or Model)
    def create(self, validated_data):
        return Product(**validated_data) 
    #With this method method we can modify (PATCH) an 
    #existing entry, we pass the entry and the new PATCH
    def update(self, instance, validate_data):
        instance.pname = validate_data.get('pname', instance.pname)
        instance.save()
        return instance
class UpdateProductSerializer(serializers.Serializer):
    id           =serializers.IntegerField(required = False) 
    pname        = serializers.CharField(max_length = 255, required = False)
    pbrand       = serializers.CharField(max_length = 255, required = False)
    pdescription = serializers.CharField(required = False)
    pstatus      = serializers.CharField(required = False)
    pcategory    = serializers.CharField(required = False)
    pprice       = serializers.DecimalField(max_digits=10, decimal_places= 2, required = False)
    pstock       = serializers.IntegerField(required = False)
    pimgspath    = serializers.FileField(required = False, allow_null = True)
    
    def update(self, instance: Product, validate_data: dict):
        instance.pname        = validate_data.get('pname')
        instance.pbrand       = validate_data.get('pbrand')
        instance.pdescription = validate_data.get('pdescription')
        instance.pstatus      = validate_data.get('pstatus')
        instance.pcategory    = validate_data.get('pcategory')
        instance.pprice       = validate_data.get('pprice')
        instance.pstock       = validate_data.get('pstock')
        instance.save()
        return instance 
 
class ImgSerializer(serializers.Serializer):
    id         = serializers.IntegerField(required = False)
    pname      = serializers.CharField(required = False) 
    pimgspath  = serializers.CharField(required = False)
    imgs_list  = serializers.ListField(required = False)
    new_imgs   = serializers.FileField(required = False)

class CustomerSerializer(serializers.Serializer):
    cid = serializers.IntegerField(read_only=True)
    cname = serializers.CharField(max_length=255)
    cphone = serializers.CharField(max_length=20)
    cemail = serializers.EmailField(max_length=255)
    cdate = serializers.DateField()

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

class UpdateCustomerSerializer(serializers.Serializer):
    cid = serializers.IntegerField(read_only=True, required = False)
    cname = serializers.CharField(max_length=255, required = False)
    cphone = serializers.CharField(max_length=20, required = False)
    cemail = serializers.EmailField(max_length=255,required = False )
    cdate = serializers.DateField(required = False)
    def update(self, instance:Customer, validate_data: dict):
        instance.cname        = validate_data.get('cname')
        instance.cphone       = validate_data.get('cphone')
        instance.cemail       = validate_data.get('cemail')
        instance.cdate        = validate_data.get('cdate')
        instance.save()
        return instance 
      

class SalesSerializer(serializers.Serializer):
    saleid    = serializers.IntegerField(required = False)
    productid = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all())
    quantity  = serializers.IntegerField()
    date      = serializers.DateField()

    def create(self, validated_data):
        return Sales(**validated_data)
    def update(self, instance: Sales, validate_data):
        instance.productid = validate_data.get('productid') 
        instance.quantity  = validate_data.get('quantity')
        instance.date      = validate_data.get('date')
        instance.save()
        return instance

class UpdateSalesSerializer(serializers.Serializer):

    productid = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all(), required = False)
    quantity  = serializers.IntegerField(required = False)
    date      = serializers.DateField(required = False)

    def update(self, instance: Sales, validate_data):
        instance.productid = validate_data.get('productid') 
        instance.quantity  = validate_data.get('quantity')
        instance.date      = validate_data.get('date')
        instance.save()
        return instance

 
        
