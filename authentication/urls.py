from django.urls import path
from .views import GetKeys,EmailUser,PhoneNumberUser


urlpatterns = [
    path('keys',GetKeys.as_view(),name="GetKeys"),
    path('email',EmailUser.as_view(),name='email user'),
    path('phone',PhoneNumberUser.as_view(),name='phone user')
]
