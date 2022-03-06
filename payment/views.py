from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from instamojo_wrapper import Instamojo
from keys import API_KEY,AUTH_TOKEN
from firebase_admin import auth,firestore


api = Instamojo(api_key=API_KEY , auth_token=AUTH_TOKEN,
                endpoint = 'https://test.instamojo.com/api/1.1/')


class Initiate(APIView):
    # def __init__(self):
    #     db = firestore.client()
        
    def post(self,request):
        db = firestore.client()
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return response(None)
        uid = info["uid"]
        user_info = db.collection("user_data").document(uid).to_dict()
        print(user_info)
        
        return Response("payment on way")    
    
    

