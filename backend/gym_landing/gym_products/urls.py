from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
router = routers.DefaultRouter()
# router.register(r'products', views.ProductsViewSet)
urlpatterns = [ 
    path('', views.product_list, name='products_list'),
    path('rest2/', views.product_listv2f, name='products_listv2'),
    path('productCR/', views.ProductCR.as_view(), name = "products_CR"),
    path('productUD/<int:pk>', views.ProductUD.as_view(), name = "products_UD"),
    #Users URL views
    path('users/', views.UserList.as_view(), name = "users_list"),
    #Product URL views
    path('products/', views.ProductList.as_view(), name = "products_list"),
    #Upload file testing      
    path('upload-file/', views.FileUploadApiView.as_view(), name = 'upload-file')
]
urlpatterns = format_suffix_patterns(urlpatterns)