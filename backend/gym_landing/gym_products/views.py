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
from .others      import handle_uploaded_file, get_all_products, filter_products
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
        if "/products/add-new-product/" == path:
            return self.add_new_product(request)
        if "products/add-new-images/"   == path:
            return Response("Yes still working on it")

    def get(self, request):
        path = request.path
      
        if "/products/get-all-products/" == path:
            all_products = get_all_products()
            return Response(all_products, status = status.HTTP_200_OK)

        if "/products/filter-products/"   == path:
            
            # filter_by = {
            #     "pstatus": [True, request ],
            #     "pprice": [True, ]
            # }        
            response = filter_products(params = request.data)
        return response
    
    def delete(self, request, pk): 
        return Response("Not done yet", status = status.HTTP_200_OK)

    def add_new_product(self, request): 
        serialize_product = ProductSerializer(data = request.data)       
        if serialize_product.is_valid():
            product_model  = serialize_product.create(serialize_product.validated_data)
            product_exists = Product.objects.filter(pname = product_model.pname).exists()

            if product_exists:
                return Response("Existing entry using the same product name!", status = status.HTTP_400_BAD_REQUEST) 
            print(f"Esta es la supuesta lista: {product_model.pimgspath}")
            product_model.pimgspath = handle_uploaded_file(
                                    request.FILES.getlist("pimgspath"))  
            product_model.save()
            return Response(serialize_product.data,
                             status = status.HTTP_200_OK) 

        return Response(serialize_product.errors,
                         status = status.HTTP_400_BAD_REQUEST)
    

