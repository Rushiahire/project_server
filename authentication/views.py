from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
from firebase_admin import auth,firestore
from .user import User

db = firestore.client() 

class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)
    

class NewUser(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)
        
        print(info["uid"])
        uid = info['uid']
        new_user = User(uid = uid)
        new_user.add_new_user()
        return Response(True)
        

class  UserInfo(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)
        
       
        uid=info['uid'] 
        user = User(uid=uid)
        data = user.fetch_info_by_id()
        return Response(data)
    
    
class UpdateAddressInfo(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        
    
        
        if(int(request.data["isMobile"]) == 1):
            info_doc = {
                "line1":request.data["line1"],
                "line2" : request.data["line2"],
                "city" : request.data["city"],
                "district" : request.data["district"],
                "state" : request.data["state"],
                "pin" : request.data["pin"]
            }

        else:
            info_doc = request.data["address"]
            
        
        uid=info['uid']
        user = User(uid = uid)
        user.update_address_id(
            value=info_doc,
            add=request.data['add'] in [True,"True","true",1],
            index= int(request.data['index']) if request.data['index'] != '' else -1
        )
        
        return Response(True)
    
    
class PaymentStatus(APIView):
    
    db = firestore.client()
    users_collection = db.collection("user_data")
    
   
    
    def post(self,request,status):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)   


        uid = info["uid"]
        user_info = self.users_collection.document(uid)
        user_info_doc = user_info.get().to_dict()
        
        payment_status_info = user_info_doc[status]
                
        return Response(payment_status_info)
      
     
                   
