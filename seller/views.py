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
    
    def post(self,request,status):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)   

        payment_info = self.status_collection.document(status)
        payment_dict = payment_info.get().to_dict()
        
        shipping_data = list()
        
        for uid in payment_dict["users"]:
            user_info = self.users_collection.document(uid).get().to_dict()
            user_info_dict = dict()    
            user_info_dict["uid"] = uid     
            for prod_info in user_info["pending"]:
                user_info_dict["address"] = prod_info["shipping_address"]
                user_info_dict["total"] = prod_info["total"]
                user_info_dict["payment_date"] = prod_info["payment_date"].strftime("%d-%m-%Y")
                user_info_dict["products"] = list()

                for product in prod_info['products']:
                    product_info = self.db.collection(product["category"]).document(product["product_id"]).get().to_dict()
                    user_info_dict["products"].append(product_info["title"])
           
            shipping_data.append(user_info_dict)  
        
        return Response(shipping_data)
    
    
    
class UpdateToDispatch(PaymentStatus):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)   
        
        
        user_uid = request.data["uid"]
        
        user_info = self.users_collection.document(user_uid)
        user_info_doc = user_info.get().to_dict()
        
        payment_status = self.status_collection.document("dispatched")
        payment_status_dict = payment_status.get().to_dict()
        
        payment_status_pending = self.status_collection.document("dispatched")
        payment_status_pending_dict = payment_status_pending.get().to_dict()
        payment_status_pending_dict["users"].remove(user_uid)
        
        payment_status_dict["users"].append(user_uid)
        print(payment_status_dict)
        
        dispatch_info = dict()
        dispatch_info["delivery_date"] = request.data["delivery_date"]
        dispatch_info["shipping_address"] = request.data["address"]
        dispatch_info["products"] = request.data["products"]
        
       
        payment_status.update({
            "users":payment_status_dict["users"]
        })
        
        payment_status_pending.update({
            "users":payment_status_pending_dict["users"]
        })
        
        user_info.update({
            "pending":list(),
            "dispatched":dispatch_info
        })
        
        return Response(True)