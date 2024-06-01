from gym_products.models import Product, User
from rest_framework import serializers
# #First way to serialize data#
# class ProductsSerializerV1(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     pname = serializers.CharField(max_length=254)
#     pdescription = serializers.CharField(max_length=254, allow_blank=True, required=False)
#     pprice = serializers.DecimalField(max_digits=9, decimal_places=2)
#     pstock = serializers.IntegerField()

#     def create(self, validated_data):
#         return Products.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.pname = validated_data.get('pname', instance.pname)
#         instance.pdescription = validated_data.get('pdescription', instance.pdescription)
#         instance.pprice = validated_data.get('pprice', instance.pprice)
#         instance.pstock = validated_data.get('pstock', instance.pstock)
#         instance.save()
#         return instance

# #Second way to serialize data#
# class ProductsSerializerV2(serializers.ModelSerializer):
#     class Meta:
#         model  = Products
#         fields = ['id', 'pname', 'pdescription', 'pprice', 'pstock']
#Third way to serialize data#
# class ProductSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model  = Product
#         fields = ('id', 'pname', 'pdescription', 'pprice', 'pstock', 'pimgpath')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model  = User
        fields = ('userid', 'uname', 'uphone', 'uemail') 

# class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta: 
#         model  = UploadedFile
#         fields = ('file', 'uploaded_on',) 


class ProductSerializer(serializers.Serializer):

    id           =serializers.IntegerField(required = False) 
    pname        = serializers.CharField(max_length = 255)
    pdescription = serializers.CharField()
    pstatus      = serializers.CharField()
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
class ImgSerializer(serializers.Serializer):
    id         = serializers.IntegerField(required = False)
    pname      = serializers.CharField(required = False) 
    pimgspath  = serializers.CharField(required = False)
    imgs_list  = serializers.ListField()
class SalesSerializer(serializers.Serializer):
    productid = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all())
    quantity  = serializers.IntegerField()
    date      = serializers.DateField()
    def create(self, validated_data):
        return Product(**validated_data)
