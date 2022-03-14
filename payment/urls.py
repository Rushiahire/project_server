from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('initiate',views.Initiate.as_view(),name="payment"),
    path('success',views.PaymentSuccess.as_view(),name="PaymentSuccess")
]
