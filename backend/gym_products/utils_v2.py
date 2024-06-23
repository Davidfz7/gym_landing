from gym_landing.settings       import MEDIA_ROOT
from .models                    import Product, Sales, Customer
#Python built-in------------------------------------------------
import os

#Rest Framework-------------------------------------------------
from rest_framework.response    import Response 
from rest_framework             import status 

#Django---------------------------------------------------------

#Gym products---------------------------------------------------
from .models                    import Product, Sales, Customer
from .serializers               import (ProductSerializer, SalesSerializer,
                                        ImgSerializer, UpdateSalesSerializer,
                                        UpdateProductSerializer, CustomerSerializer,
                                        UpdateCustomerSerializer) 

#Global methods-------------------------------------------------
def modify_files_name(directory_id:str):
    print("Estoy llegando aqui?")
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

#Views Actions--------------------------------------------------

class ProductDo():
    
    def __init__(self) -> None:
        pass
    
    #GET METHODS-------------------------------------------------
    def all_products(self) -> Response:
        query:Product = Product.objects.all()
        serializer:ProductSerializer = ProductSerializer(query, 
                                                         many = True)
        return Response(serializer.data)

    def imgs_path(self) -> Response: 
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

    def product_by_id(self, pk:int) -> Response:
        try: 
            product:Product = Product.objects.get(pk = pk)
            serializer:ProductSerializer = ProductSerializer(instance = product)      
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response({"error":"product does not exist"}, status = status.HTTP_404_NOT_FOUND)


    #POST METHODS-------------------------------------------------
    def new_product(self, request) -> Response:  
            serialize_product = ProductSerializer(data = request.data)    

            if serialize_product.is_valid():
                print(type(request.FILES))
                print(request.FILES.getlist("pimgspath"))
                print(type(request.FILES.getlist("pimgspath")))
                product_model  = serialize_product.create(serialize_product.validated_data)
                product_exists = Product.objects.filter(pname = product_model.pname).exists()

                if product_exists:
                    return Response({"error":"existing entry using the same product name"},
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
     
    def new_images(self, request, directory_id:str) -> Response:
        if request.data.get('new_imgs') is None:
            return Response({"error": "field 'new_imgs' required"}, status= status.HTTP_400_BAD_REQUEST)
        
        files_path:str = os.path.join(os.getcwd(), "media", "uploads", directory_id)
        exists:bool     = os.path.exists(files_path)
        serializer:ImgSerializer = ImgSerializer(data = request.data)
        
        if not exists:
            return Response({"info": "directory does not exist"})
        
        if serializer.is_valid():   
            files:list = request.FILES.getlist('new_imgs') 
            
            for file in files:
                file_path  = os.path.join(files_path, str(file)) 
                
                with open(file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)  
            
            modify_files_name(directory_id) 
            return Response({"info": "new images successfully added"}, status = status.HTTP_200_OK) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update_product(self, request, instance: Product) -> Response:
        required_keys = ['pname', 'pbrand', 'pdescription', 'pstatus',
                        'pcategory','pprice', 'pstock']
        values_in_instance = [instance.pname, instance.pbrand, instance.pdescription,
                            instance.pstatus, instance.pcategory, instance.pprice,
                            instance.pstock]
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
            return Response({"error": "need a field name to update or not a valid field name"}, 
                            status = status.HTTP_400_BAD_REQUEST)
    
        serializer = UpdateProductSerializer(data = request.data) 
        
        if serializer.is_valid():
            updated_product = serializer.update(instance, serializer.validated_data)
            return Response(UpdateProductSerializer(instance = updated_product).data,
                            status = status.HTTP_200_OK) 
       
        return Response(serializer.errors, status = status.HTTP_200_OK)



