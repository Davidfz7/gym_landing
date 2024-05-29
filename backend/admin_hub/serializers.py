from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)
    password = serializers.CharField(max_length=128)
   
    class Meta:
        managed = False
        db_table = 'auth_user'
    def create(self, validated_data):
        return User(**validated_data)
    def update(self, instance:User, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
