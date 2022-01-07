from django.urls import path
from .views import GetKeys,EmailUser,UpdateEmailUser,PhoneNumberUser


urlpatterns = [
    path('keys',GetKeys.as_view(),name="GetKeys"),
    path('email',EmailUser.as_view(),name='email user'),
    path('email_phone',UpdateEmailUser.as_view(),name="UpdateEmailUser"), # to update data of user logged in with email
    path('phone',PhoneNumberUser.as_view(),name='phone user')
]
