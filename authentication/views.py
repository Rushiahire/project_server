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
        
    
    def addNewUser(self,uid,user_data):
        new_user = {
            'user_id' : uid,
            'name' : user_data['user']["displayName"],
            'email' :user_data['user']['email'],
            'avatar': user_data['user']["photoURL"],
            'email_verified': user_data['user']["emailVerified"],
            'phone_number' : None,
            'phone_number_verified' : False ,
            'addresses' : [],
            'cart' : [],
            'purchase_history' : [],
            'is_seller' : False ,
            'seller_id' : None
        }
        
        new_document = self.user_data.document(uid)
        new_document.set(new_user)
        
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        isNew = request.data['userData']["additionalUserInfo"]["isNewUser"]
        
        uid = info['uid']
        
        if isNew :
            self.addNewUser(uid=uid,user_data=request.data['userData'])
        else:
            print("user already exists")
             
        
        return Response('user add')

