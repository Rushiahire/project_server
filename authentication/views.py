from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
from firebase_admin import auth,firestore
from .user import User

db = firestore.client() 

class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)
    
class EmailUser(APIView):
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        isNew = request.data['userData']["additionalUserInfo"]["isNewUser"]
        uid = info['uid']
        if isNew:
            new_user = User(uid = uid)
            new_user.add_new_user()
            return Response(True)
        return Response(False)
    
    
class PhoneUser(APIView):
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        isNew = request.data['userData'][ "_tokenResponse"]['isNewUser']
        uid = info['uid']
        if isNew:
            new_user = User(uid = uid)
            new_user.add_new_user()
            return Response(True)
        return Response(False)
        

class  UserInfo(APIView):
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        uid=info['uid']
        user = User(uid=uid)
        data = user.fetch_info_by_id()
        return Response(data)
    
    
class UpdateAddressInfo(APIView):
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        uid=info['uid']
        user = User(uid = uid)
        user.update_address_id(
            value=request.data['address'],
            add=request.data['add'],
            index= request.data['index'] if request.data['index'] != '' else request.data['index']
        )
        return Response("Updated")
      
     
                   
