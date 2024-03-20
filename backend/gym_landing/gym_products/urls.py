from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
router = routers.DefaultRouter()
# router.register(r'products', views.ProductsViewSet)
urlpatterns = [ 
    #Product URL views
    path('products/<int:pk>/', views.ProductView.as_view(), name = "product_view"),
]
urlpatterns = format_suffix_patterns(urlpatterns)