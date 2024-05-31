import jsonschema.exceptions
from gym_landing.settings       import MEDIA_ROOT
from .models                    import Product, Sales
from .serializers               import ProductSerializer, SalesSerializer, ImgSerializer 
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

def filter_products(params: dict):
    # {
    #     "filter_by": [], -> add columns that you wish to filter by
    #     "values": {
    #         "pprice_values": [], -> add prices that you wish to filter by(max 
    #                                 values = 2, is a range)
    #         "pstock_values": [], -> add stock values that you wish to filter by(
    #                                  max values = 2, is a range)
  
    #         "pstatus_values": [] -> add pstatus values that you wish to filter by(
    #                                  max values = 2, is a range)
    #     },
    #     "sort_reference": value, -> field value that you wish to use the sort function (asc or desc)
    #     "sort_elements_ascendant": value, -> bool value
    #     "sort_elements_descendant": value, -> bool value
    # }


   
    # if not valid_json_stucture(params ,params.get("values")):
    #     return Response("Not a valid json", status = status.HTTP_400_BAD_REQUEST)
    is_valid = validate_json_stucture(params)
    if not is_valid:
        return Response("Not a valid json stucture")
    return Response("Testing till here") 
    fields         = params.get("filter_by")
    values         = params.get("values")
    
    pprices_values = values.get("pprice_values")
    pstock_values  = values.get("pstock_values")
    pstatus_values = values.get("pstatus.values")

                            #Related
   #-----------------------------------------------------------------
    sort_reference = params.get("sort_reference")
    ascendant      = params.get("sort_elements_ascendant") 
    descendant     = params.get("sort_elements_descendant")
 
    if ascendant or descendant:
        return descen_or_ascen(ascendant, descendant,
                               sort_reference, values)
   #-----------------------------------------------------------------
    # if "pprice" in fields and "pprice":
    #     product    = Product.objects.filter(
    #                         pprice = values[0]) 
    #     serializer = ProductSerializer(product, many = True)
    #     return serializer.data 
    return "Hello david"

def descen_or_ascen(ascendant: bool, descendant: bool,field: str, values: dict) -> Response:
    #Check if valid values
    valid_fields = ["pstatus", "pprice", "pstock"]

    if field not in valid_fields:
        return Response("Not a valid sort reference", status = status.HTTP_400_BAD_REQUEST)
    
    if ascendant:
        ascendant_objects = Product.objects.all().order_by(field)
        serializer        = ProductSerializer(ascendant_objects, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    elif descendant:
        descendant_objects = Product.objects.all().order_by(f"-{field}")
        serializer         = ProductSerializer(descendant_objects, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK) 

def validate_json_stucture(filter_json: dict) -> bool:
    schema = {
        "type": "object",
        "properties": {
            "filter_by": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["pstatus", "pprice", "pstock"]
            }
        },
        "values": {
            "type": "object",
            "properties": {
                "pprice_values": {
                    "type": "array",
                    "items": {
                        "type": "number",
                    },
                    "maxItems": 2
                },
                "pstock_values": {
                    "type": "array",
                    "items": {
                        "type": "number", 
                    },
                    "maxItems": 2 
                },
                "pstatus_values": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["available", "out of stock", "coming soon"]
                    }
                }
            },
        },
        "sort_reference": {
            "type": "string",
            "enum": ["pprice", "pstatus", "pstock"]
        },
        "sort_elements_ascendant": {
            "type": "boolean"
        },
        "sort_elements_descendant": {
            "type": "boolean"
        }
    },
    "required":["filter_by"],
    "not":{
        "allOf":[
            {"properties": {"sort_elements_ascendant": {"const": True } } },
            {"properties": {"sort_elements_descendant":  {"const": True } } }
            ]
        }
    }
    try: 
        validate(instance=filter_json, schema= schema)
    except jsonschema.exceptions.ValidationError as err:
       print(err)
       return False

    return True 

def add_new_product(request): 
       
        serialize_product = ProductSerializer(data = request.data)    

        if serialize_product.is_valid():
            print(type(request.FILES))
            print(request.FILES.getlist("pimgspath"))
            print(type(request.FILES.getlist("pimgspath")))
            product_model  = serialize_product.create(serialize_product.validated_data)
            product_exists = Product.objects.filter(pname = product_model.pname).exists()

            if product_exists:
                return Response("Existing entry using the same product name!", status = status.HTTP_400_BAD_REQUEST) 
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

def modify_files_name(directory_id:str):
    files_path = os.path.join(os.getcwd(), "media", "uploads", directory_id)
    exists     = os.path.exists(files_path)
    print(files_path)
    if not exists:
        return "No existing path"
    count = 1
    for file in os.listdir(files_path):
        file_split = file.split(".")
        print(file_split)
        old_name   = os.path.join(files_path, file)
        new_name   = os.path.join(files_path, f"img{str(count)}.{file_split[1]}") 
        if os.path.isfile(new_name):
            count += 1
            print("Entre aqui para hacer el continue xD")
            continue
        os.rename(old_name, new_name)
        count    += 1 
    return "All file names updated"
    
def add_new_sale(request):
    print(type(request.data))
    if not isinstance(request.data, dict):
        return Response(f"Need a json structure {SALES_SCHEMA}", status = status.HTTP_400_BAD_REQUEST)
    data = dict(request.data)
    if not validate_sale_post(data):
        return Response(f"Not a valid json: {SALES_SCHEMA}", 
                        status = status.HTTP_400_BAD_REQUEST)
    try:
        product   = Product.objects.get(pk = data.get("productid"))
        new_sale  = Sales(productid = product, quantity = data.get("quantity"), 
                          date = data.get("date")) 
        new_sale.save()
        serialize = SalesSerializer(new_sale)
        return Response(serialize.data, status = status.HTTP_200_OK)
    except Product.DoesNotExist as err:
        return Response(str(err), status = status.HTTP_400_BAD_REQUEST)

def validate_sale_post(data: dict):
    try:
        validate(instance = data, schema = SALES_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError as err:
        return False

def get_imgs_path(): 
    products_with_pimgspath = Product.objects.filter(pimgspath__isnull=False)
    product_values = products_with_pimgspath.values('pname', 'pimgspath')
    for dict in product_values:
        directory_id =  str(dict.get('pimgspath')).split("/")
        files_path = os.path.join(os.getcwd(), "media", "uploads", f"{directory_id[1]}") 
        if not os.path.exists(files_path):
            dict.update({"imgs_list": []})
        else:
            dict.update({"imgs_list": os.listdir(files_path)})
    serializer = ImgSerializer(instance = product_values, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK) 