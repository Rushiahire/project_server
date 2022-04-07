
from django.urls import path

from .views import GetKeys,UserInfo,UpdateAddressInfo,PaymentStatus,NewUser


urlpatterns = [
    path('keys',GetKeys.as_view(),name="GetKeys"),
    path('new_user',NewUser.as_view(),name="NewUser"),
    path('info',UserInfo.as_view(),name="userInfo"),
    path('update_address',UpdateAddressInfo.as_view(),name="UpdateAddressInfo"),
    path('payment/<str:status>',PaymentStatus.as_view(),name="PaymentStatus")
]
