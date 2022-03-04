from django.urls import path
from .views import FetchProduct,ProductDetails,AddReview,FetchReview,UpdateCart,FetchCart,CartBill



urlpatterns=[
    path('fetch/<str:category>',FetchProduct.as_view(),name='fetch'),
    path('detail/<str:category>/<str:key>',ProductDetails.as_view(),name='product details'),
    path('review',AddReview.as_view(),name='add_review'),
    path('viewreview/<str:category>/<str:key>',FetchReview.as_view(),name="FetchReview"),
    path('update_cart',UpdateCart.as_view(),name="UpdateCart"),
    path('get_cart',FetchCart.as_view(),name="FetchCart"),
    path('bill',CartBill.as_view(),name="CartBill")
]


