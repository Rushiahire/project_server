from django.urls import path
from .import views



urlpatterns=[
    path('fetch',views.FetchProduct.as_view(),name='fetch'),
    path('detail/<str:key>',views.ProductDetails.as_view(),name='product details')
]


