from typing import Any
from django.http                  import Http404
#----------------------------------------------
from rest_framework.parsers     import JSONParser
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework.parsers     import FormParser, MultiPartParser, JSONParser 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
#----------------------------------------------
from .models      import Product, Customer, Sales
from .serializers import ProductSerializer, CustomerSerializer, SalesSerializer
from .utils      import  (get_all_sales, add_new_sale, update_sale, 
                           add_customer, get_all_customers,
                           update_customer)

from .utils_v2 import *
#----------------------------------------------

       
class ProductView(APIView): 
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ProductSerializer
    #permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    #authentication_classes = [TokenAuthentication]
    permission_classes = []
    authentication_classes = []

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.product_do:ProductDo = ProductDo() 
    
    def get_object(self, pk): 
        try: 
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk:int = None):
        path = request.path

        if "/all-products/" == path:
            rp:Response = self.product_do.all_products()
            return rp

        if f"/product/{pk}/" == path:
            rp:Response = self.product_do.product_by_id(pk)
            return rp

        if "/imgs-names/" == path:
            rp:Response = self.product_do.imgs_path()
            return rp 
        
    def post(self, request, pk = None):
        path = request.path

        if "/new-product/" == path:
            rp:Response = self.product_do.new_product(request)
            return rp
        
        if f"/new-images/{pk}/" == path:
            product: Product  = self.get_object(pk)
            rp = self.product_do.new_images(request = request, 
                                            directory_id = str(product.id))
            return rp 
         
    def patch(self, request, pk:int = None):
        path = request.path

        if f"/update-product/{pk}/" == path: 
            product:Product = self.get_object(pk)
            rp:Response = self.product_do.update_product(request = request,
                                                        instance = product)
            return rp
        return Response({"error": "not valid endpoint"}, 
                        status = status.HTTP_400_BAD_REQUEST)     
 
class SaleView(APIView):
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
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

    def patch(self, request, pk = None):
        try: 
            sale = Sales.objects.get(pk = pk)
            return update_sale(request, sale)
        except Sales.DoesNotExist:
            return Response({"info": "Sale not found"}, status = status.HTTP_404_NOT_FOUND)
    def delete(self, request, pk = None):
        try: 
            sale = Sales.objects.get(pk = pk)
            sale.delete()
            return Response({"info": "Sale deleted"}, status= status.HTTP_200_OK)
        except Sales.DoesNotExist:
            return Response({"info": "Sale not found"}, status = status.HTTP_404_NOT_FOUND)
        

class CustomerView(APIView):
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk): 
        try: 
            return Customer.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404
   
    def get(self, request, pk = None):
        path = request.path
        if path == '/get-all-customers/':
            return get_all_customers()
        if f"/get-customer/{pk}/" == path: 
            try: 
                product = Customer.objects.get(pk = pk)
                serializer = CustomerSerializer(instance= product)      
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response({"info":"Customer does not exist"}, status = status.HTTP_404_NOT_FOUND) 
        return Response("customerview.get()", status = status.HTTP_200_OK)    
    def patch(self, request, pk = None):
        try: 
            product = Customer.objects.get(pk = pk)
            return update_customer(instance = product,
                                   request = request) 
        except Customer.DoesNotExist:
            return Response({"info":"Customer does not exist"}, status = status.HTTP_404_NOT_FOUND) 
    
    def delete(self, request, pk = None):
        try: 
            customer = Customer.objects.get(pk = pk)
            customer.delete()
            return Response({"info": "Customer deleted"}, status= status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"info": "Customer not found"}, status = status.HTTP_404_NOT_FOUND) 

class AddCustomerView(APIView):
    parser_classes   = (MultiPartParser, FormParser, JSONParser)     
    def post(self, request):
        path = request.path
        if "/add-customer/" == path:
            return add_customer(request) 
        return Response("addcustomerview.post()", status = status.HTTP_200_OK)