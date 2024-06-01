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
    path("get-all-products/", views.ProductViewNoAuth.as_view(),  name = "get_all_products"),
    path("add-new-sale/", views.SaleView().as_view(), name = "add_new_sale"),
    path("get-all-sales/" ,views.SaleView.as_view(), name = "get_all_sales"),
    path("get-product/<int:pk>/",  views.ProductViewNoAuth.as_view(),  name = "filter_products"),
    path("get-imgs-names/", views.ProductViewNoAuth.as_view(), name = "get_imgs_paths"),
    path("update-sale/<int:pk>/", views.SaleView.as_view(), name = "update_sale"),
    path("delete-sale/<int:pk>/", views.SaleView.as_view(), name = "delete_sale")
] 


urlpatterns = format_suffix_patterns(urlpatterns)