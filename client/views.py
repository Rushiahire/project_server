# from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import firestore,auth
# from project_server.project_server.settings import CACHE_TTL
# import datetime
# from links import STORAGE_BUCKET_URL
from seller.product import Product
from authentication.user import User
# from products_common import laptops,iphone,camera,clock,watch
# import random
# from django.conf import settings
# from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
from django.core.cache import cache


# CACHE_TTL = getattr(settings,"CACHE_TTL",DEFAULT_TIMEOUT)


class FetchProduct(APIView):
    
    def get_homepage_contents(self,category):
        # for index,category in enumerate(categories):
        db = firestore.client()
        category_collection = db.collection(category)
        product_list = category_collection.stream()
        data_array = list()
        for product_doc in product_list:
            doc = product_doc.to_dict()
            data = {
                'thumbnail' : doc['thumbnail_image']['url'],
                'price' : doc['price'],
                'title' : doc['title'],
                # 'category':category,
                # 'quantity' : doc['quantity'],
                'key': product_doc.id
            }
            data_array.append(data)
        return data_array
    
    # def get_homepage_category(self,category):
    #     if category == 'laptop':
    #         array_length = 6 if len(laptops) >= 6 else len(laptops)
    #         return random.sample(laptops,array_length)
    #     if category == "camera":
    #         array_length = 6 if len(camera) >= 6 else len(camera)
    #         return random.sample(camera,array_length)
    #     if category == "clock":
    #         array_length = 6 if len(clock) >= 6 else len(clock)
    #         return random.sample(clock,array_length)
    #     if category == "watch":
    #         array_length = 6 if len(watch) >= 6 else len(watch)
    #         return random.sample(watch,array_length)
    #     if category == "iphone":
    #         array_length = 6 if len(iphone) >= 6 else len(iphone)
    #         return random.sample(iphone,array_length)
    
    def get(self,request,category):
        if cache.get(category):
            # print("comming from cache",category)
            product_list = cache.get(category)
        else:
            # print("comming from database")
            product_list = self.get_homepage_contents(category=category)
            cache.set(category,product_list)
            # print("cached into memory now",category)
        return Response(product_list)
    
    
class ProductDetails(APIView):
    def get(self,request,category,key):
        info = Product()
        data = info.get_info_by_id(key=key,is_history=True,category=category)
        return Response(data)
    
    
class AddReview(APIView):
    db = firestore.client()
    product_info = db.collection('product_info')
        
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        
        
        # print(info["email"])
        product_info = self.db.collection(request.data["category"])
        product_id = request.data['id']
        doc = product_info.document(product_id)
        
        doc_data = doc.get().to_dict()
        review_list = doc_data['reviews']
        new_review = {
            'user': info["email"],
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
    def get(self,request,category,key):
        product_info = self.db.collection(category)
        doc = product_info.document(key).get().to_dict()
        return Response(doc['reviews'])
    
    
class UpdateCart(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        
        uid = info['uid']
        user = User(uid = uid)
        
        product_info = {
           
            "product_id" : request.data['product_id'],
            "quantity" : request.data['quantity'],
            "price" : request.data["price"]
        }

        if(request.data['add']):
             product_info["category"] = request.data["category"]
        
        
        user.update_cart(
            product_info = product_info,
            add = request.data['add'],
            index = request.data['index'],
            is_qty = request.data['is_qty']
        )
        return Response(True)
    
class FetchCart(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(False)
        
        uid = info['uid']
        user = User(uid=uid)
        cart = user.get_cart_by_id()
        return Response(cart)
    
    
class CartBill(APIView):
    def post(self,request):
        try:
            info = auth.verify_id_token(request.data['idToken'])
        except:
            return Response(None)

        uid = info['uid']
        user = User(uid=uid)
        data = user.get_total_by_id()
        return Response(data)
