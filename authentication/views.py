from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
from firebase_admin import auth,firestore


class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)


class User(APIView):
    # def __init__(self):
    #     self.user_data = firestore.collection('user_data')
        
    # UserId
    # Name
    # Email 
    # Email varified ?
    # phone number
    # phone number
    # phone number varified ?
    # addresses = []
    # cart = []
    # purchase history = []
    # id_seller ? (false by default)
    # seller_id = null/None (by Default)
    
        
        
    def post(self,request):
        # print(request.data)
        info = auth.verify_id_token(request.data['idToken'])
        print(info)
        # print(response.text)
        return Response('user add')

