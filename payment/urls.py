from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path("keys",views.RazorPayKeys.as_view(),name="RazorPayKeys"),
    path('success',views.PaymentSuccess.as_view(),name="PaymentSuccess"),
]
