
from django.urls import path

from .views import GetKeys,EmailUser,PhoneUser,UserInfo,UpdateAddressInfo


urlpatterns = [
    path('keys',GetKeys.as_view(),name="GetKeys"),
    path('email',EmailUser.as_view(),name='email user'),
    # path('email_phone',UpdateEmailUser.as_view(),name="UpdateEmailUser"), # to update data of user logged in with email
    path('phone',PhoneUser.as_view(),name='phone user'),
    path('info',UserInfo.as_view(),name="userInfo"),
    path('update_address',UpdateAddressInfo.as_view(),name="UpdateAddressInfo")
]
