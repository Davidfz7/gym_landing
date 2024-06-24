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

from .utils import *
#----------------------------------------------

       
class ProductView(APIView): 
    parser_classes   = (MultiPartParser, FormParser, JSONParser) 
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
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    permission_classes = []
    authentication_classes = []

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.sale_do:SaleDo = SaleDo()

    def get(self, request):
        path = request.path
 
        if "/all-sales/" == path:
            rp:Response = self.sale_do.all_sales()
            return rp
        return Response({"error": "not a valid endpoint"},
                        status = status.HTTP_404_NOT_FOUND)

    def post(self, request):
        path = request.path
        
        if "/new-sale/" == path: 
            rp:Response = self.sale_do.new_sale(request = request)
            return rp 
        
        return Response({"error": "not a valid endpoint"},
                        status = status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk:int = None):
        path = request.path

        if f"/update-sale/{pk}/" == path:
            try: 
                sale = Sales.objects.get(pk = pk)
                return self.sale_do.update_sale(request, sale)
            except Sales.DoesNotExist:
                return Response({"info": "sale not found"}, status = status.HTTP_404_NOT_FOUND)

        return Response({"error": "not a valid endpoint"},
                        status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk:int = None):
        path = request.path

        if f"/delete-sale/{pk}/" == path:
            try: 
                sale = Sales.objects.get(pk = pk)
                rp:Response = self.sale_do.delete_sale(request = request,
                                                    instance = sale)
                return rp
            except Sales.DoesNotExist:
                return Response({"error": "sale does not exist"}, 
                                status = status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "not a valid endpoint"},
                        status = status.HTTP_404_NOT_FOUND)

class CustomerView(APIView):
    parser_classes   = (MultiPartParser, FormParser, JSONParser)
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    permission_classes = []
    authentication_classes = []

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.customer_do:CustomerDo = CustomerDo()

    def get_object(self, pk): 
        try: 
            return Customer.objects.get(pk = pk)
        except Product.DoesNotExist:
            raise Http404
   
    def get(self, request, pk = None):
        path = request.path
        
        if path == '/all-customers/':
            rp:Response = self.customer_do.all_customers()
            return rp 
        
        if f"/customer/{pk}/" == path: 
            rp:Response = self.customer_do.customer_id(pk=pk)
            return rp 
        
        return Response({"error": "not a valid endpoint"}, status = status.HTTP_400_BAD_REQUEST)    
    
    def post(self, request):
        path = request.path
        
        if "/new-customer/" == path:
            rp:Response = self.customer_do.new_customer(request = request)
            return rp 

        return Response({"error":"not a valid endpoint"}, 
                       status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk:int = None):
        path = request.path

        if f"/update-customer/{pk}/" == path:
            try: 
                customer = Customer.objects.get(pk = pk)
                rp:Response = self.customer_do.update_customer(instance = customer,
                                                            request = request)
                return rp 
            except Customer.DoesNotExist:
                return Response({"info":"customer does not exist"}, status = status.HTTP_404_NOT_FOUND) 
        
        return Response({"error":"not a valid endpoint"}, 
                       status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk:int = None):
        path = request.path

        if f"/delete-customer/{pk}/" == path:
            rp:Response = self.customer_do.delete_customer(pk = pk)
            return rp

        return Response({"error": "not a valid endpoint"}, 
                        status = status.HTTP_400_BAD_REQUEST) 