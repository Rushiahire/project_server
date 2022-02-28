from rest_framework.views import APIView
from rest_framework.response import Response
from .product import Product
from keys import adminFirebaseConfig
from firebase_admin import auth


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
