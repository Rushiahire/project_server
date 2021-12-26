from django.urls import path
from .import views



urlpatterns=[
    path('fetch',views.FetchProduct.as_view(),name='fetch')
]


