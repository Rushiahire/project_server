from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from instamojo_wrapper import Instamojo
from keys import API_KEY,AUTH_TOKEN
from firebase_admin import auth,firestore
from links import PAYMENT_REDIRECT_URL


api = Instamojo(
    api_key=API_KEY ,
    auth_token=AUTH_TOKEN,
    endpoint = 'https://test.instamojo.com/api/1.1/'
    )


class Initiate(APIView):
        
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
        # print(user_data)
        try:
            payment_response = api.payment_request_create(
                amount=user_info["total"] + 50,
                purpose="shopping from ShopHeaven",
                send_email=True,
                email=email,
                redirect_url=PAYMENT_REDIRECT_URL  
            )
            print(payment_response)
        except :
            return Response(None)
        # print(payment_response)
        
        
        return Response(payment_response['payment_request']['longurl'])