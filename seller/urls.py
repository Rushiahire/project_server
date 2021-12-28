from django.urls import path
from .views import NewProduct,SellerPanel,DeleteProduct


urlpatterns = [
    path('addproduct',NewProduct.as_view(),name="NewProduct"),
    path('panel',SellerPanel.as_view(),name='sellerpanel'),
    path('deleteproduct',DeleteProduct.as_view(),name='deleteproduct')
]