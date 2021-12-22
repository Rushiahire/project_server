from django.urls import path
from .views import NewProduct

urlpatterns = [
    path('addproduct',NewProduct.as_view(),name="NewProduct")
]