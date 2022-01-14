from rest_framework.response import Response
from rest_framework.views import APIView
from keys import firebaseConfig
from firebase_admin import auth,firestore


db = firestore.client() 

class GetKeys(APIView):
    def get(self,request):
        return Response(firebaseConfig)
    
    
class User():
    
    user_data = db.collection('user_data')
    
    def __init__(self,uid=''):
        self.uid = uid  
        
    def add_new_user(self):
        new_document = self.user_data.document(self.uid)
        new_data = {
            "uid" : self.uid,
            "addresses" : list(),
            "cart" : list(),
            "purchase_history" : list(),
            "is_seller" : False,
            "seller_id" : None
        }
        new_document.set(new_data)
        
    def fetch_info_by_id(self):
        user_data_document = self.user_data.document(self.uid).get().to_dict()
        return user_data_document
    
    def delete_by_id(self):
        self.user_data.document(self.uid).delete()
        return "deleted"
    
    def update_address_id(self,value,add,index=-1):
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        
        if add:
            user_doc['addresses'].append(value)
        else:
            del(user_doc['addresses'][index])
        
        user_info.update({
                'addresses':user_doc['addresses']
        })
            
        
        
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
        # print(request.data)
        info = auth.verify_id_token(request.data['idToken'])
        uid=info['uid']
        user = User(uid=uid)
        data = user.fetch_info_by_id()
        return Response(data)
    
    
class UpdateAddressInfo(APIView):
    def post(self,request):
        # print(request.data)
        info = auth.verify_id_token(request.data['idToken'])
        uid=info['uid']
        user = User(uid = uid)
        user.update_address_id(
            value=request.data['address'],
            add=request.data['add'],
            index= request.data['index'] if request.data['index'] != '' else request.data['index']
        )
        return Response("Updated")
      
     
                   

# class EmailUser(APIView):
#     def __init__(self):
#         self.db = firestore.client() 
#         self.user_data = self.db.collection('user_data')
        
    
#     def addNewUser(self,uid,user_data):
#         new_user = {
#             'user_id' : uid,
#             # 'name' : user_data['user']["displayName"],
#             # 'email' :user_data['user']['email'],
#             # 'avatar': user_data['user']["photoURL"],
#             # 'email_verified': user_data['user']["emailVerified"],
#             'phone_number' : None,
#             'phone_number_verified' : False ,
#             'addresses' : [],
#             'cart' : [],
#             'purchase_history' : [],
#             'is_seller' : False ,
#             'seller_id' : None
#         }
        
#         new_document = self.user_data.document(uid)
#         new_document.set(new_user)
        
#     def post(self,request):
#         info = auth.verify_id_token(request.data['idToken'])
#         isNew = request.data['userData']["additionalUserInfo"]["isNewUser"]
        
#         uid = info['uid']
        
#         if isNew :
#             self.addNewUser(uid=uid,user_data=request.data['userData'])
#         return Response(isNew)
    
    
# class UpdateEmailUser(EmailUser):
#     def post(self,request):
#         print(request.data.keys())
#         return Response("hahahaha")


# class PhoneNumberUser(EmailUser):
#     def post(self,request):
#         print(request.data['userData'][ "_tokenResponse"]['isNewUser'])
#         return Response(request.data['userData'][ "_tokenResponse"]['isNewUser'])