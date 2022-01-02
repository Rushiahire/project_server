from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
import requests
from keys import API_KEY

class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)


class User(APIView):
    def post(self,request):
        # print(request.data['userData']['credential']['idToken'])
        
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup"
        payload = {
            # 'key' : request.data['userData']['credential']['idToken']
            "key": f"{API_KEY}={request.data['userData']['credential']['idToken']}"

        }
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
            
        }        
        response = requests.post(url,headers=headers , data=payload )
        
        print(response.text)
        
        
        return Response('user add')
