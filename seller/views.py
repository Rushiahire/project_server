import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .product import Product
from keys import adminFirebaseConfig
from firebase_admin import auth,firestore


class SellerAuthKeys(APIView):
    def get(self,request):
        return Response(adminFirebaseConfig)


class NewProduct(APIView):

    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        new_product = Product()
        new_product.add_new_product(request_data=request)
        return Response(True)
    
class SellerPanel(APIView):    
    def get(self,request,category):
        products = Product()
        product_list = products.get_product_list(category=category)
        return Response(product_list)
    
    
class DeleteProduct(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        product = Product()
        product.delete_product(request_data=request)
        return Response(True)
    

class UpdateProduct(APIView):
    def post(self,request): 
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)    
        current_product = Product()
        current_product.update_product(request_data=request)
        return Response(True)
    
    
    
class PaymentStatus(APIView):
    
    db = firestore.client()
    status_collection = db.collection("payment_data")
    users_collection = db.collection("user_data")
    
    def get_pending_info(self):
        payment_info = self.status_collection.document("pending")
        payment_dict = payment_info.get().to_dict()
        # print(payment_dict)            
            
        return payment_dict["users"]
    
    def get_dispatch_status(self):
        payment_info = self.status_collection.document("dispatched")
        payment_dict = payment_info.get().to_dict()
        # print(payment_dict)            
        return payment_dict["users"]

    
    def post(self,request,status):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)   


        if status == "pending":
            pending_info = self.get_pending_info()
            return Response(pending_info)
        
        if status == "dispatched":
            dispatch_info = self.get_dispatch_status()
            print(dispatch_info)
            return Response(dispatch_info)
        
        # if request.data["status"] == "delivered":
        #     pass
        
        # payment_info = self.status_collection.document(status)
        # payment_dict = payment_info.get().to_dict()
        
        # shipping_data = list()
        
        return Response(None)
    
    
    
class UpdateToDispatch(PaymentStatus):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)   
        
        user_uid = request.data["user_info"]["uid"]
        
        user_info = self.users_collection.document(user_uid)
        user_info_doc = user_info.get().to_dict()
        pending_info = self.status_collection.document("pending")
        pending_info_doc = pending_info.get().to_dict()
        
        pending_info_doc["users"].remove(request.data["user_info"])
        user_info_doc["pending"].remove(request.data["user_info"])
        
        current_transaction = dict()
        
        current_transaction["user_info"] = request.data["user_info"]
        current_transaction["delivery_date"] = request.data["order_date_by_seller"]
        
        user_info_doc["dispatched"].append(current_transaction)
        print("Dispatched : ",user_info_doc["dispatched"])
        print("Pending : ",user_info_doc["pending"])
        
        payment_info = self.status_collection.document("dispatched")
        payment_info_dict = payment_info.get().to_dict()
        
        payment_info_dict["users"].append(current_transaction)
        
        user_info.update({
            "pending":user_info_doc["pending"],
            "dispatched":user_info_doc["dispatched"]
        })
        
        pending_info.update({
            "users":pending_info_doc["users"]
        })
        
        payment_info.update({
            "users":payment_info_dict["users"]
        })
        
        
        return Response(True)