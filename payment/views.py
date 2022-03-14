from mimetypes import init
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from instamojo_wrapper import Instamojo
from keys import API_KEY,AUTH_TOKEN
from firebase_admin import auth,firestore
from links import PAYMENT_REDIRECT_URL
from authentication.user import User


api = Instamojo(
    api_key=API_KEY ,
    auth_token=AUTH_TOKEN,
    endpoint = 'https://test.instamojo.com/api/1.1/'
    )


class Initiate(APIView):
    
    def initiate_payment(self,email,user_info):
        try:
            if user_info["total"] > 0:
                payment_response = api.payment_request_create(
                    amount=user_info["total"] + 50,
                    purpose="shopping from ShopHeaven",
                    send_email=False,
                    email=email,
                    redirect_url=PAYMENT_REDIRECT_URL  
                )
                print(payment_response)
            else:
                return None
        except :
            return None
        
        return payment_response['payment_request']
        
        
    def post(self,request):
        db = firestore.client()
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return response(None)
        uid = info["uid"]
        user_info = db.collection("user_data").document(uid).get().to_dict()
        user_data = auth.get_user(uid)
        email = user_data.email
        payment_info = self.initiate_payment(email=email,user_info=user_info)
       
    
        return Response(payment_info)
    
    
class PaymentSuccess(APIView):
    def post(self,request):
        
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)
        
        uid = info["uid"]
        user = User(uid=uid)
        payment_id = request.data["payment_id"]
        payment_id_local = request.data["payment_id_local"]
       
        user.move_cart_to_pending(
            payment_id=payment_id,
            payment_id_local = payment_id_local,
            shipping_address = request.data["shipping_address"]
        )
        
        return Response(True)