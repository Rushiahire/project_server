from django.urls import path
from .views import FetchProduct,ProductDetails,AddReview,FetchReview,UpdateCart,FetchCart



urlpatterns=[
    path('fetch',FetchProduct.as_view(),name='fetch'),
    path('detail/<str:key>',ProductDetails.as_view(),name='product details'),
    path('review',AddReview.as_view(),name='add_review'),
    path('viewreview/<str:key>',FetchReview.as_view(),name="FetchReview"),
    path('update_cart',UpdateCart.as_view(),name="UpdateCart"),
    path('get_cart',FetchCart.as_view(),name="FetchCart")
]


