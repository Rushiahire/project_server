from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
from firebase_admin import auth,firestore


class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)


class User(APIView):
    def __init__(self):
        self.db = firestore.client() 
        self.user_data = self.db.collection('user_data')
        
        
        
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
    
    def addNewUser(self,user_data):
        new_user = {
            'user_id' : '',
            'name' : '',
            'email' : '',
            'email_verified': False ,
            'phone_number' : '',
            'phone_number_verified' : False ,
            'addresses' : '',
            'cart' : '',
            'purchase_history' : '',
            'id_seller' : False ,
            'seller_id' : ''
        }
        
        new_document = self.user_data.document('user_id')
        new_document.set(new_user)
        
    def post(self,request):
        # print(request.data)
        info = auth.verify_id_token(request.data['idToken'])
        print(auth.list_users())    
        # print(response.text)
        return Response('user add')

