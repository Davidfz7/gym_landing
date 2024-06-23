import jsonschema.exceptions
from gym_landing.settings       import MEDIA_ROOT
from .models                    import Product, Sales, Customer
from .serializers               import (ProductSerializer, SalesSerializer,
                                        ImgSerializer, UpdateSalesSerializer,
                                        UpdateProductSerializer, CustomerSerializer,
                                        UpdateCustomerSerializer) 
from rest_framework.response    import Response 
from rest_framework             import status 
from itertools                  import zip_longest
import os

from jsonschema import validate
import jsonschema

SALES_SCHEMA = {
  "type": "object",
  "properties": {
    "productid": {
      "type": "integer"
    },
    "quantity": {
      "type": "integer"
    },
    "date": {
      "type": "string"
    }
  },
  "required": [
    "productid",
    "quantity",
    "date"
  ]
} 
#For Post requests
#--------------------------------------------------
def handle_file_directories() -> list:
    """
        It creates a directory for the file in case that is a new product otherwise
        it returns the path for the specified product
    """

    count_products    = Product.objects.count() +1 
    absolute_path = f"{MEDIA_ROOT}/uploads/{count_products}/"
    relative_path = f"uploads/{count_products}/"
        
    if os.path.exists(absolute_path):
        return "Files exists"

    os.makedirs(absolute_path)
    return [relative_path, absolute_path]

def handle_uploaded_file(files: list) -> str:
    """
        This method is just for saving the file following this structure:
        uploads/{model pk}/{file_name.ext}
    """
    paths_list = handle_file_directories()
    absolute_path = paths_list[1] 
    relative_path = paths_list[0]
    print(f"This are the files: {files}")
    print(f'This is the relative path -> {relative_path}')
    for file in files:
        print(f"Este es el supuesto file {file}")
        with open(f'{absolute_path}/{str(file)}', 'wb') as destination: 
            for chunk in file.chunks():
                destination.write(chunk)
    return relative_path
#------------------------------------------------------

def get_all_products():
    query      = Product.objects.all()
    serializer = ProductSerializer(query, many = True)
    return serializer.data

def add_new_product(request): 
       
        serialize_product = ProductSerializer(data = request.data)    

        if serialize_product.is_valid():
            print(type(request.FILES))
            print(request.FILES.getlist("pimgspath"))
            print(type(request.FILES.getlist("pimgspath")))
            product_model  = serialize_product.create(serialize_product.validated_data)
            product_exists = Product.objects.filter(pname = product_model.pname).exists()

            if product_exists:
                return Response("Existing entry using the same product name!",
                                status = status.HTTP_400_BAD_REQUEST) 

            product_model.pimgspath = handle_uploaded_file(
                                    request.FILES.getlist("pimgspath"))  
            product_model.save()
            
            modify_files_name(str(product_model.id))
            return Response(serialize_product.data,
                             status = status.HTTP_200_OK) 
        print(serialize_product.errors)
        return Response(serialize_product.errors,
                         status = status.HTTP_400_BAD_REQUEST)
    

def get_all_sales():
    query      = Sales.objects.all()
    serializer = SalesSerializer(query, many = True)
    return serializer.data


    
def add_new_sale(request):
    serializer = SalesSerializer(data = request.data) 
    if serializer.is_valid():
        new_sale = serializer.create(serializer.validated_data)
        new_sale.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def validate_sale_post(data: dict):
    try:
        validate(instance = data, schema = SALES_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError as err:
        return False

def get_imgs_path(): 
    products_with_pimgspath = Product.objects.filter(pimgspath__isnull=False)
    product_values = products_with_pimgspath.values('id','pname', 'pimgspath')
    for dict in product_values:
        directory_id =  str(dict.get('pimgspath')).split("/")
        files_path = os.path.join(os.getcwd(), "media", "uploads", f"{directory_id[1]}") 
        if not os.path.exists(files_path):
            dict.update({"imgs_list": []})
        else:
            dict.update({"imgs_list": os.listdir(files_path)})
    serializer = ImgSerializer(instance = product_values, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def update_sale(request, instance: Sales):
    required_keys = ['productid', 'quantity', 'date']
    values_in_instance = [instance.productid.id, 
                          instance.quantity, str(instance.date)]
    data_dict:dict = request.data
    count_a = 0
    count_b = 0
    for key in required_keys:
        if key not in data_dict.keys():
            count_a += 1
            data_dict.update({key: values_in_instance[count_b]})      
        count_b += 1  
    if count_a == 3:
        return Response({"error": "Need a field name to update or not a valid field name"}, status= status.HTTP_400_BAD_REQUEST)
    serializer  = UpdateSalesSerializer(data = request.data) 
    if serializer.is_valid():
        updated_sale = serializer.update(instance, serializer.validated_data)  
        return Response(SalesSerializer(instance = updated_sale).data,
                        status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)





def add_customer(request):
    customer_data:dict = request.data 
    serializer:CustomerSerializer = CustomerSerializer(data = customer_data)
    if serializer.is_valid():
        new_customer:Customer = serializer.create(serializer.validated_data) 
        return Response(CustomerSerializer(instance = new_customer).data, 
                        status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_200_OK)
def get_all_customers():
    try:
        all_customers = Customer.objects.all()
        serializer = CustomerSerializer(instance = all_customers, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({'error': 'Customers not found'}, 
                        status = status.HTTP_404_NOT_FOUND)
    
def update_customer(instance: Customer, request):
    required_keys = ['cname', 'cphone', 'cemail', 'cdate']
    values_in_instance = [instance.cname, instance.cphone,
                           instance.cemail, str(instance.cdate)]
    data_dict:dict = request.data
    count_a = 0
    count_b = 0
    for key in required_keys:
        if key not in data_dict.keys():
            count_a += 1
            if values_in_instance[count_b] is None:
                count_b += 1 
                continue
            data_dict.update({key: values_in_instance[count_b]})
        count_b += 1
    if count_a == len(required_keys):
        return Response({"error": "Need a field name to update or not a valid field name"}, 
                        status = status.HTTP_400_BAD_REQUEST)
   
    serializer = UpdateCustomerSerializer(data = request.data) 
    if serializer.is_valid():
        updated_product = serializer.update(instance, serializer.validated_data)
        return Response(UpdateCustomerSerializer(instance = updated_product).data,
                        status = status.HTTP_200_OK) 
    return Response(serializer.errors, status = status.HTTP_200_OK)
    
    
