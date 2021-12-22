from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response


class Homepage(APIView):
    def get(self,request):
        helpertext={
            'homepage':'/',
            'view_all_carts':'viewcart',
            'details_view':'detail/<str:key>'
        }
        return Response(helpertext)