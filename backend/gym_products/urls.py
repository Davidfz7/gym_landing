from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
router = routers.DefaultRouter()
# router.register(r'products', views.ProductsViewSet)
urlpatterns = [ 
    #Product URL views
    path("", views.ProductView.as_view()),

    #PRODUCT ENDPOINTS --------------------------------------------------------------------    
    path("new-product/",  views.ProductView.as_view(),  name = "add_new_product"),
    path("update-product/<int:pk>/", views.ProductView.as_view(), name = "update_product"),
    path("new-images/<int:pk>/", views.ProductView.as_view(), name = "add_new_images"),
    path("all-products/", views.ProductView.as_view(),  name = "get_all_products"),
    path("product/<int:pk>/",  views.ProductView.as_view(),  name = "filter_products"),
    path("imgs-names/", views.ProductView.as_view(), name = "get_imgs_paths"),

    #SALES ENDPOINTS------------------------------------------------------------------------
    path("new-sale/", views.SaleView().as_view(), name = "add_new_sale"),
    path("update-sale/<int:pk>/", views.SaleView.as_view(), name = "update_sale"),
    path("delete-sale/<int:pk>/", views.SaleView.as_view(), name = "delete_sale"),
    path("all-sales/" ,views.SaleView.as_view(), name = "get_all_sales"),
    
    #CUSTOMER ENDPOINTS--------------------------------------------------------------------- 
    path("new-customer/", views.CustomerView.as_view(), name   = "new_customer"),
    path("all-customers/", views.CustomerView.as_view(), name = "all_customers"),
    path("customer/<int:pk>/", views.CustomerView.as_view(), name = "customer_id"),
    path("delete-customer/<int:pk>/", views.CustomerView.as_view(), name = "delete_customer"),
    path("update-customer/<int:pk>/", views.CustomerView.as_view(), name = "update_customer")
] 


urlpatterns = format_suffix_patterns(urlpatterns)