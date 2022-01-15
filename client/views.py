from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import storage,firestore,auth
import datetime
from links import STORAGE_BUCKET_URL
from seller.product import Product
from authentication.user import User


class FetchProduct(APIView):
    def get(self,request):
        product_info = Product()
        product_list = product_info.get_product_list()
        return Response(product_list)
    
    
class ProductDetails(APIView):
    def get(self,request,key):
        info = Product()
        data = info.get_info_by_id(key=key,is_history=True)
        return Response(data)
    
    
class AddReview(APIView):
    db = firestore.client()
    product_info = db.collection('product_info')
        
    def post(self,request):
        product_id = request.data['id']
        doc = self.product_info.document(product_id)
        
        doc_data = doc.get().to_dict()
        review_list = doc_data['reviews']
        new_review = {
            'title':request.data['title'],
            'description':request.data['description'],
            'rating':int(request.data['rating'])
        }
        review_list.append(new_review)
        
        doc.update({
            'reviews': review_list
        })
        
        return Response("Review added successfully")
    
    
class FetchReview(AddReview):
    def get(self,request,key):
        doc = self.product_info.document(key).get().to_dict()
        return Response(doc['reviews'])
    
    
class UpdateCart(APIView):
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        uid = info['uid']
        user = User(uid = uid)
        product_info = {
            "product_id" : request.data['product_id'] ,
            "quantity" : request.data['quantity']
        }
        user.update_cart(
            product_info = product_info,
            add = request.data['add'],
            index = request.data['index'],
            is_qty = request.data['is_qty']
        )
        print(info['uid'])
        return Response("done dona done")
    
class FetchCart(APIView):
    def post(self,request):
        info = auth.verify_id_token(request.data['idToken'])
        uid = info['uid']
        user = User(uid=uid)
        cart = user.get_cart_by_id()
        return Response(cart)
