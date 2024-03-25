from gym_landing.settings       import MEDIA_ROOT
from .models                    import Product
from .serializers               import ProductSerializer 
from rest_framework.response    import Response 
from rest_framework             import status 
from itertools                  import zip_longest
import os

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
    # params = {
    #     "filter_by": ["pprice"],
    #     "values": [22.0]
    # }
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

    if not valid_json_stucture(params ,params.get("values")):
        return Response("Not a valid json", status = status.HTTP_400_BAD_REQUEST)
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

def valid_json_stucture(outer_dict: dict, inner_dict: dict) -> bool:
    schema = {
        "type": "object",
        "properties":{
            "filter_by": {"type": "list"},
            "values":    {"type": "dict"},
            "sort_reference": {"type": "string"},
            "sort_elements_ascendant": {"type": "bool"},
            "sort_elements_descendant": {"type": "bool"}
        },
        "required": ["filter_by"]
    }
    outer_filter_keys   = ["filter_by", "values",
                      "sort_reference", "sort_elements_ascendant",
                      "sort_elements_descendant"]
    inner_filter_keys   = ["pprice_values", "pstock_values",
                           "pstatus_values"]

    outer_dict_keys  = list(outer_dict.keys())
    inner_dict_keys = list(inner_dict.keys())

    for outer_key, inner_key in zip_longest(outer_dict_keys, inner_dict_keys):
        if outer_key not in outer_filter_keys:
            return False
        if inner_key == None:
            continue
        if inner_key not in inner_filter_keys:
            return False
    

    return True 

