from django.urls import path
from .views import NewProduct,SellerPanel,DeleteProduct,UpdateProduct,SellerAuthKeys


urlpatterns = [
    path('addproduct',NewProduct.as_view(),name="NewProduct"),
    path('panel',SellerPanel.as_view(),name='sellerpanel'),
    path('deleteproduct',DeleteProduct.as_view(),name='deleteproduct'),
    path('update',UpdateProduct.as_view(),name='UpdateProduct'),
    path('keys',SellerAuthKeys.as_view(),name="SellerAuthKeys")
]