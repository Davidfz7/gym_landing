from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
router = routers.DefaultRouter()
# router.register(r'products', views.ProductsViewSet)
urlpatterns = [ 
    #Product URL views
    path("", views.ProductView.as_view()),
    path("add-new-product/",  views.ProductView.as_view(),  name = "add_new_product"),
    path("get-all-products/", views.ProductView.as_view(),  name = "get_all_products"),
    path("filter-products/",  views.ProductView.as_view(),  name = "filter_products"),
] 


urlpatterns = format_suffix_patterns(urlpatterns)