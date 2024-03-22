from django.http                  import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http                  import Http404
from gym_landing.settings         import MEDIA_ROOT
#----------------------------------------------
from rest_framework.parsers     import JSONParser
from rest_framework             import status
from rest_framework.decorators  import api_view, permission_classes
from rest_framework.response    import Response
from rest_framework             import permissions
from rest_framework.views       import APIView
from rest_framework             import mixins
from rest_framework             import generics
from rest_framework.parsers     import FormParser, MultiPartParser, FileUploadParser, JSONParser 
#----------------------------------------------
from .models      import Product, User
from .serializers import ProductSerializer, UserSerializer
#----------------------------------------------
import os
import json
       
class ProductView(APIView):

    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ProductSerializer
    def get_object(self , pk):
        try: 
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404


    def post(self, request):
        serialize_product = ProductSerializer(data = request.data)
        count_products    = Product.objects.count()
        if serialize_product.is_valid():
            product_model  = serialize_product.create(serialize_product.validated_data)
            product_exists = Product.objects.filter(pname = product_model.pname).exists()
           
            if product_exists:
                return Response("Existing entry using the same product name!", status = status.HTTP_400_BAD_REQUEST) 
            
            product_model.save()
            return Response(ProductSerializer(product_model).data,
                             status = status.HTTP_200_OK) 
 
        print(serialize_product.errors)

        return Response(serialize_product.errors, status = status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            letMeSee = serializer.create(serializer.validated_data)
            letMeSee.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
        
        print(serializer.errors)
        return Response("Not valid", status = status.HTTP_200_OK)
        #print(request.data)




