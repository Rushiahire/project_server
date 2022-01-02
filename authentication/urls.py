from django.urls import path
from .views import GetKeys,User


urlpatterns = [
    path('keys',GetKeys.as_view(),name="GetKeys"),
    path('user',User.as_view(),name='user')
]
