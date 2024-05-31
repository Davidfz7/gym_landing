from django.http                  import Http404
#----------------------------------------------
from rest_framework.parsers     import JSONParser
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework.parsers     import FormParser, MultiPartParser, JSONParser 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
#----------------------------------------------
from .models      import Product, User
from .serializers import ProductSerializer, CustomerSerializer
from .others      import  (get_all_products,filter_products, 
                           add_new_product, get_all_sales, add_new_sale,
                           get_imgs_path)
#----------------------------------------------

       
class ProductView(APIView): 
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]     
   
    def get_object(self, pk):
        
        try: 
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404
        
    def post(self, request):
        path = request.path
        if "/add-new-product/" == path:
            return add_new_product(request)
        if "/add-new-images/"   == path:
            return Response("Yes still working on it")

    def delete(self, request, pk): 
        return Response("Not done yet", status = status.HTTP_200_OK)

class ProductViewNoAuth(APIView):
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ProductSerializer
   
 
    def get(self, request, pk = None):
        path = request.path
        if "/get-all-products/" == path:
            all_products = get_all_products()
            return Response(all_products, status = status.HTTP_200_OK)
        if "/get-imgs-paths/" == path: 
            return get_imgs_path() 
        if pk is not None: 
            try: 
                product = Product.objects.get(pk = pk)
                serializer = ProductSerializer(instance= product)      
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"info":"Product does not exist"}, status = status.HTTP_404_NOT_FOUND)
        
 
class SaleView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        path = request.path
        if "/get-all-sales/" == path:
            print("si entro aqui")
            all_sales = get_all_sales()
            return Response(all_sales, status = status.HTTP_200_OK)
    
    def post(self, request):
        path = request.path
        if "/add-new-sale/" == path: 
            return add_new_sale(request)