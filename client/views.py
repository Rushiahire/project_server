from itertools import product
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import firestore,auth
from seller.product import Product
from authentication.user import User
from django.core.cache import cache
import random
import math


class FetchProduct(APIView):
    
    def get_homepage_contents(self,category):
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
                'key': product_doc.id
            }
            data_array.append(data)
        return data_array
    

    def get(self,request,category):
        if cache.get(category):
            product_list = cache.get(category)
        else:
            product_list = self.get_homepage_contents(category=category)
            cache.set(category,product_list[:5])
        return Response(product_list[:5])
    
    
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
        
        product_info = self.db.collection(request.data["category"])
        product_id = request.data['id']
        doc = product_info.document(product_id)
        
        doc_data = doc.get().to_dict()
        review_list = doc_data['reviews']
        new_review = {
            # 'user': info["email"],
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
        # print(request.data)
        # info = auth.verify_id_token(request.data['idToken'])
        try:
            # print("verifing idToken")
            # print(request.data)
            info = auth.verify_id_token(request.data['idToken'])
            # print("Done")
        except:
            # print()
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
        add = ""
        is_qty = ""
        if request.data["add"] in [1,True,"True","true"]:
            add = True
        else:
            add = False
              
        if request.data["is_qty"] in [1,True,"True","true"]:
            is_qty = True
        else:
            is_qty = False
        
        user.update_cart(
            product_info = product_info,
            add = add,
            index = int(request.data['index']),
            is_qty = is_qty
        )
        # print("addded to cart")
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
    
    
class CategoryInfo(APIView):
    def get(self,request,category,page_number):
        elements_per_page = 10
        start_index = elements_per_page * (int(page_number)-1)
        end_index = elements_per_page * (int(page_number)) 
        
        category_key = f"{category}{page_number}"
        number_of_pages_cache_label = f"cache{category}number_of_pages"
        
        if cache.get(category_key):
            product_list = cache.get(category_key)
            number_of_pages = cache.get(number_of_pages_cache_label)
        else:
            prodcut = Product()
            product_list = prodcut.get_product_list(category)
            number_of_pages = math.ceil(len(product_list)/elements_per_page)
            if len(product_list) > 0:
                product_list = product_list[start_index:end_index]
                cache.set(category_key,product_list)
                cache.set(number_of_pages_cache_label,number_of_pages)
        
        data = {
            "product_list" : product_list,
            "number_of_pages":number_of_pages
        }
        
        return Response(data)
