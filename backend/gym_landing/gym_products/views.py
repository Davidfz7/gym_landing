from django.http                  import Http404
#----------------------------------------------
from rest_framework.parsers     import JSONParser
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework.parsers     import FormParser, MultiPartParser, JSONParser 
#----------------------------------------------
from .models      import Product, User
from .serializers import ProductSerializer, UserSerializer
from .others      import  get_all_products, filter_products, add_new_product
#----------------------------------------------

       
class ProductView(APIView):
    """
        Whole path that we are going to be using:
        products/{function name}
    """
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ProductSerializer
    
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

    def get(self, request):
        path = request.path
      
        if "/get-all-products/" == path:
            all_products = get_all_products()
            return Response(all_products, status = status.HTTP_200_OK)

        if "/filter-products/"   == path:
            response = filter_products(params = request.data)
        return response
    
    def delete(self, request, pk): 
        return Response("Not done yet", status = status.HTTP_200_OK)


    

