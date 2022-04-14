from rest_framework.views import APIView
from rest_framework.response import Response
from keys import RZ_KEY,RZ_SECRETE
from firebase_admin import auth
from authentication.user import User


class RazorPayKeys(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)
        
        keys = {
            "api_key" : RZ_KEY,
            "api_secrete" : RZ_SECRETE 
        }
        
        return Response(keys);
    
class PaymentSuccess(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)
        
        
        uid = info["uid"]
        user = User(uid=uid)
        payment_id = request.data["payment_id"]
       
        user.move_cart_to_pending(
            payment_id=payment_id,
            shipping_address = int(request.data["shipping_address"])
        )
        
        return Response(True)
    
    


    
