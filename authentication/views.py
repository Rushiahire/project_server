from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig

class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)

