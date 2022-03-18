from django.urls import path
from .views import NewProduct,SellerPanel,DeleteProduct,UpdateProduct,SellerAuthKeys,PaymentStatus,UpdateToDispatch,UpdateToDelivered


urlpatterns = [
    path('addproduct',NewProduct.as_view(),name="NewProduct"),
    path('panel/<str:category>/<str:page_number>',SellerPanel.as_view(),name='sellerpanel'),
    path('deleteproduct',DeleteProduct.as_view(),name='deleteproduct'),
    path('update',UpdateProduct.as_view(),name='UpdateProduct'),
    path('keys',SellerAuthKeys.as_view(),name="SellerAuthKeys"),
    path("payment/<str:status>",PaymentStatus.as_view(),name="PaymentStatus"),
    path("dispatch",UpdateToDispatch.as_view(),name="UpdateToDispatch"),
    path("delivered",UpdateToDelivered.as_view(),name="UpdateToDelivered")
]