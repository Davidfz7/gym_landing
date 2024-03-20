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
from rest_framework.parsers     import FormParser, MultiPartParser, FileUploadParser 
#----------------------------------------------
from .models      import Product, User
from .serializers import ProductSerializer, UserSerializer
#----------------------------------------------
import os
import json
       
class ProductView(APIView):

    parser_classes   = (MultiPartParser, FormParser)
    serializer_class = ProductSerializer
    def get_object(self , pk):
        try: 
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        product    = self.get_object(pk)
        whoYouAre  = self.serializer_class( product)
        serializer = self.serializer_class(instance = product, data = request.data)
        if serializer.is_valid():
           
           print(serializer)

        return Response(whoYouAre.data, status = status.HTTP_400_BAD_REQUEST) 




