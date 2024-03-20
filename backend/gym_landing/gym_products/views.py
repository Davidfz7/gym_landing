from django.http                  import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http                  import Http404
#----------------------------------------------
from rest_framework.parsers     import JSONParser
from rest_framework             import status
from rest_framework.decorators  import api_view, permission_classes
from rest_framework.response    import Response
from rest_framework             import permissions
from rest_framework.views       import APIView
from rest_framework             import mixins
from rest_framework             import generics
from rest_framework.parsers     import FormParser, MultiPartParser 
#----------------------------------------------
from .models      import Product, User
from .serializers import ProductSerializer, UserSerializer, FileUploadSerializer
# Create your views here.
def saveSomethin(request):
    if request.method == 'POST':
        return HttpResponse("Post request")
    if request.method == 'GET':
        return HttpResponse("Get request")
    # Product = Product()
    # Product.pname = "test"
    # Product.pdescription = "description"
    # Product.pprice = 23.2
    # Product.pstock = 2
    # Product.save()
    return HttpResponse("Nice")

@csrf_exempt
def product_list(request):
    """
    request -> classic django request object
    List all Product
    """
    if request.method == 'GET':
        print(f"Request object type{type(request)}")
        # Product = Product.objects.all()
        # serializer = ProductSerializer(Product, many = True)
        return HttpResponse("hOla") 
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
    return JsonResponse(serializer.errors, status = 400)

#View using django rest framework features

@api_view(['GET', 'POST', 'PUT', 'DELETE']) #-> Converts this function in a ApiView subclass
@permission_classes((permissions.AllowAny,))
def product_listv2f(request):

    """
    request -> django_rest_framework Request Object
    Response -> similar to HttpResponse but better
    List all Product, version 2
    """
 
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many = True)
        return Response(serializer.data) 

    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#@permission_classes((permissions.AllowAny))          
class ProductCR(APIView):
    """
        Simple Create and Read for Product Model
    """
    def get(self, request, format=None):
        Product   = Product.objects.all()
        serializer = ProductSerializer(Product, many=True) 
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status = status.HTTP_201_CREATED)
        return Response (serializer.errors, status= status.HTTP_400_BAD_REQUEST) 
    
class ProductUD(APIView):
    """
        Simple Update and Delete for Product Model
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404
 
    def put(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        serializer = ProductSerializer(product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        product = self.get_object(pk)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
class ProductList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 


class FileUploadApiView(APIView):
    parser_classes   = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status = status.HTTP_201_CREATED
        )


