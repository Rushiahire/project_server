from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
import requests
from keys import API_KEY
from firebase_admin import auth
import json


class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)


class User(APIView):
    def post(self,request):
        # print(request.data)
        
        info = auth.verify_id_token(request.data['idToken'])
        
        print(info)
        
        # print(response.text)
        
        
        return Response('user add')
