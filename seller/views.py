import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .product import Product
from keys import adminFirebaseConfig
from firebase_admin import auth,firestore
from django.core.cache import cache
import math

from payment.payment_status import update_pending_to_dispatch,update_dispatch_to_delivered


class SellerAuthKeys(APIView):
    def get(self,request):
        return Response(adminFirebaseConfig)


class NewProduct(APIView):

    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        
        key = f'seller{request.data["category"]}'
        if cache.get(key):
            cache.delete_many(keys=cache.keys(key))
        
        new_product = Product()
        new_product.add_new_product(request_data=request)
        return Response(True)
    
class SellerPanel(APIView):    
    def get(self,request,category,page_number):
        elements_per_page = 5
        start_index = elements_per_page * (int(page_number)-1)
        end_index = elements_per_page * (int(page_number)) 
                       
        products = Product()
        product_list = products.get_product_list(category=category)
        number_of_pages = math.ceil(len(product_list)/elements_per_page)
        product_list = product_list[start_index:end_index]
        
        data = {
            "product_list" : product_list,
            "number_of_pages" : number_of_pages
        }
        
        return Response(data)
    
    
class DeleteProduct(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        
        key = f'seller{request.data["category"]}'
        if cache.get(key):
            cache.delete_many(keys=cache.keys(key))
        
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
            
        return payment_dict["users"]
    
    def get_dispatch_status(self):
        payment_info = self.status_collection.document("dispatched")
        payment_dict = payment_info.get().to_dict()          
        return payment_dict["users"]
    
    
    def get_delivered_status(self):
        payment_info = self.status_collection.document("delivered")
        payment_dict = payment_info.get().to_dict()
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
            return Response(dispatch_info)
        
        if status == "delivered":
            dekivered_info = self.get_delivered_status()
            return Response(dekivered_info)
        
        return Response(None)
    
    
    
class UpdateToDispatch(PaymentStatus):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)   
        
        user_uid = request.data["user_info"]["uid"]
        update_pending_to_dispatch(
                data=request.data,
                uid=user_uid
            )
               
        
        return Response(True)
    
    
class UpdateToDelivered(PaymentStatus):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False) 
        
        update_dispatch_to_delivered(
            data=request.data,
            uid=request.data["user_data"]["user_info"]["uid"]
        )
        
        
        return Response(True)