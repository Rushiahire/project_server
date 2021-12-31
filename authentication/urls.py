from django.urls import path
from .views import GetKeys


urlpatterns = [
    path('keys',GetKeys.as_view(),name="GetKeys")
]
