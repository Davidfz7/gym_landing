from gym_products.models import Product, User, UploadedFile
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
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Product
        fields = ('id', 'pname', 'pdescription', 'pprice', 'pstock')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model  = User
        fields = ('userid', 'uname', 'uphone', 'uemail') 

class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model  = UploadedFile
        fields = ('file', 'uploaded_on',) 